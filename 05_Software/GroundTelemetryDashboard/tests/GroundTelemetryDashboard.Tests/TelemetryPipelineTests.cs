using System.Diagnostics;
using System.Security.Cryptography;
using System.Text.Json;
using GroundTelemetryDashboard.Core.Models;
using GroundTelemetryDashboard.Core.Parsing;
using GroundTelemetryDashboard.Core.Stats;
using GroundTelemetryDashboard.Web.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;

namespace GroundTelemetryDashboard.Tests;

public sealed class TelemetryPipelineTests
{
    [Fact]
    public void ParserAcceptsVersionedV4Packet()
    {
        const string line =
            "4,305419896,7,1200,1,3,100,-100,16384,5,-6,7,1,0,0,0,10";

        var ok = SerialLineParser.TryParseCsvLine(
            line,
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.Equal(4, sample.ProtocolVersion);
        Assert.Equal(305419896, sample.BootId);
        Assert.Equal(7, sample.Seq);
        Assert.Equal(1, sample.SensorType);
        Assert.Equal(3, sample.QualityFlags);
        Assert.Equal(10, sample.DtMs);
        Assert.True(sample.IsScientificQuality);
        Assert.Equal("v4-12345678", sample.SessionId);
    }

    [Theory]
    [InlineData("4,1,1,1,1,1,NaN,0,0,0,0,0,1,0,0,0,10", "NONFINITE_OR_INVALID_NUMBER")]
    [InlineData("4,1,1,1,1,1,40000,0,0,0,0,0,1,0,0,0,10", "SENSOR_RANGE")]
    [InlineData("5,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,10", "VERSIONED_HEADER")]
    [InlineData("4,1,1,1,1,0,0,0,0,0,0,1,0,0,0", "V4_REQUIRES_SENSOR_AND_DT")]
    public void ParserRejectsStructurallyInvalidFrames(
        string line,
        string expectedError)
    {
        var ok = SerialLineParser.TryParseCsvLine(
            line,
            out var sample,
            out var error);

        Assert.False(ok);
        Assert.Null(sample);
        Assert.Equal(expectedError, error);
    }

    [Theory]
    [InlineData("4,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,10", "IMU_NOT_VALID")]
    [InlineData("4,1,1,1,1,4,0,0,0,0,0,0,1,0,0,0,10", "UNKNOWN_QUALITY_FLAGS")]
    [InlineData("4,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,10", "UNKNOWN_SENSOR_TYPE")]
    [InlineData("4,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0", "DT_MS_RANGE")]
    [InlineData("4,1,1,1,1,1,0,0,0,0,0,0,2,0,0,0,10", "QUATERNION_NORM")]
    public void ParserRetainsLinkFrameButRejectsScientificAdmission(
        string line,
        string expectedValidationCode)
    {
        var ok = SerialLineParser.TryParseCsvLine(
            line,
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.False(sample.IsScientificQuality);
        Assert.Equal(expectedValidationCode, sample.ScientificValidationCode);
    }

    [Fact]
    public void ParserRetainsRawLegacyCompatibility()
    {
        var ok = SerialLineParser.TryParseCsvLine(
            "7,1200,100,-100,16384,5,-6,7",
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.Equal(1, sample.ProtocolVersion);
        Assert.Equal(1, sample.Q0);
        Assert.False(sample.IsScientificQuality);
    }

    [Theory]
    [InlineData("1,0,7,1200,0,0,100,-100,16384,5,-6,7,1,0,0,0,0", 1)]
    [InlineData("2,0,7,1200,0,0,100,-100,16384,5,-6,7,1,0,0,0,10", 2)]
    [InlineData("3,0,7,1200,1,0,100,-100,16384,5,-6,7,1,0,0,0,10", 3)]
    public void ParserAcceptsReceiverNormalizedLegacyPackets(
        string line,
        int version)
    {
        var ok = SerialLineParser.TryParseCsvLine(
            line,
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.Equal(version, sample.ProtocolVersion);
        Assert.False(sample.IsScientificQuality);
    }

    [Fact]
    public void StatsDoNotCountRebootAsPacketLoss()
    {
        var calculator = new StatsCalculator(TimeSpan.FromMinutes(1));
        calculator.RegisterSample(Sample(100, 10, 1000));
        calculator.RegisterSample(Sample(100, 13, 2500));
        var afterReboot = calculator.RegisterSample(Sample(200, 0, 20));

        Assert.Equal(2, afterReboot.LinkLostCountEstimated);
        Assert.Equal(2, afterReboot.SessionCount);
        Assert.Equal(0, afterReboot.LinkLostCountWindow);
        Assert.Equal(0, afterReboot.LastSeq);
    }

    [Fact]
    public void StatsSeparateDuplicateOutOfOrderAndWrap()
    {
        var calculator = new StatsCalculator(TimeSpan.FromMinutes(1));
        calculator.RegisterSample(Sample(1, uint.MaxValue - 1, 100));
        calculator.RegisterSample(Sample(1, uint.MaxValue, 200));
        calculator.RegisterSample(Sample(1, 0, 300));
        calculator.RegisterSample(Sample(1, 0, 301));
        var stats = calculator.RegisterSample(Sample(1, uint.MaxValue, 302));

        Assert.Equal(0, stats.LinkLostCountEstimated);
        Assert.Equal(1, stats.DuplicateCount);
        Assert.Equal(1, stats.OutOfOrderCount);
        Assert.Equal(0, stats.LastSeq);
    }

    [Fact]
    public void StatsRejectTimeRegressionFromSeries()
    {
        var calculator = new StatsCalculator(TimeSpan.FromMinutes(1));
        calculator.RegisterSampleDetailed(Sample(1, 1, 1000));
        var regressed =
            calculator.RegisterSampleDetailed(Sample(1, 2, 900));
        var recovered =
            calculator.RegisterSampleDetailed(Sample(1, 3, 1100));

        Assert.False(regressed.AcceptedForSeries);
        Assert.Equal("TIME_REGRESSION", regressed.ScientificDisposition);
        Assert.Equal(1, regressed.Stats.TimeRegressionCount);
        Assert.True(recovered.AcceptedForSeries);
        Assert.Equal(0, recovered.Stats.LinkLostCountEstimated);
        Assert.Equal(0, recovered.Stats.LinkPerWindow);
        Assert.Equal(2, recovered.Stats.ScientificAdmittedCount);
        Assert.Equal(1, recovered.Stats.ScientificRejectedCount);
    }

    [Fact]
    public void InvalidImuQualityCountsAsReceivedButNotScientific()
    {
        var calculator = new StatsCalculator(TimeSpan.FromMinutes(1));
        var invalid = calculator.RegisterSampleDetailed(
            Sample(1, 10, 1000, qualityFlags: 0));
        var valid = calculator.RegisterSampleDetailed(
            Sample(1, 11, 1100));

        Assert.Equal("RECEIVED_SESSION_START", invalid.LinkDisposition);
        Assert.Equal("IMU_NOT_VALID", invalid.ScientificDisposition);
        Assert.False(invalid.AcceptedForSeries);
        Assert.Equal(1, invalid.Stats.LinkReceivedCount);
        Assert.Equal(0, invalid.Stats.LinkLostCountEstimated);
        Assert.Equal(0, invalid.Stats.LinkPerWindow);
        Assert.Equal(0, invalid.Stats.ScientificAdmittedCount);
        Assert.Equal(1, invalid.Stats.ScientificRejectedCount);
        Assert.Equal(0, invalid.Stats.ScientificYieldWindow);

        Assert.True(valid.AcceptedForSeries);
        Assert.Equal(2, valid.Stats.LinkReceivedCount);
        Assert.Equal(0, valid.Stats.LinkLostCountEstimated);
        Assert.Equal(1, valid.Stats.ScientificAdmittedCount);
        Assert.Equal(1, valid.Stats.ScientificRejectedCount);
        Assert.Equal(0.5, valid.Stats.ScientificYieldWindow);
    }

    [Fact]
    public void ConnectionGenerationForcesPortReopen()
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["Serial:BaudRate"] = "115200"
            })
            .Build();
        var manager = new SerialConnectionManager(configuration);

        var first = manager.Connect("COM1", 115200);
        var second = manager.Connect("COM2", 57600);

        Assert.True(second.Generation > first.Generation);
        Assert.Equal("COM2", second.PortName);
        Assert.Equal(57600, second.Baud);
        Assert.False(manager.Disconnect(first.Generation));
        Assert.Equal("REQUESTED", manager.GetStatus().State);
        Assert.True(manager.MarkOpening(second.Generation));
        Assert.True(manager.MarkOpen(second.Generation));
        Assert.True(manager.GetStatus().IsConnected);
        Assert.True(manager.Disconnect(second.Generation));
    }

    [Fact]
    public void EvidenceBundleIsClosedAnchoredAndTamperEvident()
    {
        var root = Path.Combine(
            Path.GetTempPath(),
            $"australis-ground-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(root);
        try
        {
            var configuration = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["Evidence:Enabled"] = "true",
                    ["Evidence:Root"] = root,
                    ["Evidence:SourceCommit"] =
                        "0123456789abcdef0123456789abcdef01234567"
                })
                .Build();
            var environment = new TestHostEnvironment(root);
            string evidenceFile;
            string runDirectory;

            using (var recorder = new EvidenceRecorder(
                       configuration,
                       environment,
                       NullLogger<EvidenceRecorder>.Instance))
            {
                recorder.RecordRawLine("diagnostic line");
                var sample = Sample(1, 1, 1);
                var registration =
                    new StatsCalculator().RegisterSampleDetailed(sample);
                recorder.RecordSample(sample, registration);
                runDirectory = recorder.RunDirectory!;
                evidenceFile = Path.Combine(runDirectory, "evidence.jsonl");

                var active = EvidenceVerifier.VerifyBundle(
                    runDirectory,
                    requireClosed: false);
                Assert.True(active.IsValid, active.Error);
                Assert.Equal("ACTIVE_PREFIX_VALID", active.State);
            }

            var valid = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);
            Assert.True(valid.IsValid, valid.Error);
            Assert.Equal(4, valid.RecordCount);
            Assert.Equal("COMPLETE_LOCAL_SEAL_VALID", valid.State);

            var configurationFile =
                Path.Combine(runDirectory, "configuration.json");
            var originalConfiguration =
                File.ReadAllText(configurationFile);
            File.WriteAllText(
                configurationFile,
                originalConfiguration + " ");
            var configurationTampered = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);
            Assert.False(configurationTampered.IsValid);
            Assert.Equal(
                "CONFIGURATION_SNAPSHOT_MISMATCH",
                configurationTampered.Error);
            File.WriteAllText(configurationFile, originalConfiguration);

            var original = File.ReadAllText(evidenceFile);
            var lines = File.ReadAllLines(evidenceFile);
            File.WriteAllLines(evidenceFile, lines[..^1]);
            var truncated = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);
            Assert.False(truncated.IsValid);
            Assert.Equal("RUN_CLOSE_MISSING", truncated.Error);

            File.WriteAllText(evidenceFile, original);
            File.WriteAllText(
                evidenceFile,
                original.Replace(
                    "raw_serial_line",
                    "tampered_serial_line",
                    StringComparison.Ordinal));
            var tampered = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);
            Assert.False(tampered.IsValid);
            Assert.StartsWith("HASH:", tampered.Error);
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }

    [Fact]
    public void EvidenceRejectsEmptyChain()
    {
        var empty = Path.GetTempFileName();
        try
        {
            var result = EvidenceVerifier.VerifyFile(empty);
            Assert.False(result.IsValid);
            Assert.Equal("EMPTY_CHAIN", result.Error);
        }
        finally
        {
            File.Delete(empty);
        }
    }

    [Fact]
    public void MatchingSealCannotPromotePrefixWithoutRunClose()
    {
        var root = Path.Combine(
            Path.GetTempPath(),
            $"australis-ground-prefix-{Guid.NewGuid():N}");
        Directory.CreateDirectory(root);
        try
        {
            var configuration = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["Evidence:Enabled"] = "true",
                    ["Evidence:Root"] = root,
                    ["Evidence:SourceCommit"] =
                        "0123456789abcdef0123456789abcdef01234567"
                })
                .Build();
            string runDirectory;
            using (var recorder = new EvidenceRecorder(
                       configuration,
                       new TestHostEnvironment(root),
                       NullLogger<EvidenceRecorder>.Instance))
            {
                recorder.RecordRawLine("prefix-only");
                runDirectory = recorder.RunDirectory!;
            }

            var evidencePath = Path.Combine(runDirectory, "evidence.jsonl");
            var lines = File.ReadAllLines(evidencePath);
            File.WriteAllLines(evidencePath, lines[..^1]);
            using var finalRecord = JsonDocument.Parse(lines[^2]);
            var finalSha = finalRecord.RootElement
                .GetProperty("sha256").GetString();
            var manifestPath = Path.Combine(runDirectory, "manifest.json");
            using var manifest = JsonDocument.Parse(
                File.ReadAllText(manifestPath));
            var runId = manifest.RootElement
                .GetProperty("run_id").GetString();
            var forgedSeal = new
            {
                run_id = runId,
                record_count = lines.Length - 1,
                final_record_sha256 = finalSha,
                manifest_sha256 = Sha256File(manifestPath),
                evidence_file_sha256 = Sha256File(evidencePath)
            };
            File.WriteAllText(
                Path.Combine(runDirectory, "bundle_seal.json"),
                JsonSerializer.Serialize(forgedSeal));

            var result = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);

            Assert.False(result.IsValid);
            Assert.Equal("RUN_CLOSE_MISSING", result.Error);
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }

    [Fact]
    public void RunCloseCountMustMatchActualChainLength()
    {
        var root = Path.Combine(
            Path.GetTempPath(),
            $"australis-ground-close-count-{Guid.NewGuid():N}");
        Directory.CreateDirectory(root);
        try
        {
            var configuration = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["Evidence:Enabled"] = "true",
                    ["Evidence:Root"] = root,
                    ["Evidence:SourceCommit"] =
                        "0123456789abcdef0123456789abcdef01234567"
                })
                .Build();
            string runDirectory;
            using (var recorder = new EvidenceRecorder(
                       configuration,
                       new TestHostEnvironment(root),
                       NullLogger<EvidenceRecorder>.Instance))
            {
                recorder.RecordRawLine("close-count");
                runDirectory = recorder.RunDirectory!;
            }

            var evidencePath = Path.Combine(runDirectory, "evidence.jsonl");
            var lines = File.ReadAllLines(evidencePath);
            using var close = JsonDocument.Parse(lines[^1]);
            var rootElement = close.RootElement;
            var index = rootElement.GetProperty("index").GetInt64();
            var atUtc = rootElement.GetProperty("atUtc").GetDateTime();
            var monotonicTicks =
                rootElement.GetProperty("monotonicTicks").GetInt64();
            var previousSha = rootElement
                .GetProperty("previousSha256").GetString()!;
            var runId = rootElement.GetProperty("payload")
                .GetProperty("run_id").GetString();
            var payloadJson = JsonSerializer.Serialize(
                new { run_id = runId, final_record_count = 999L });
            using var payloadDocument = JsonDocument.Parse(payloadJson);
            var replacementHash = EvidenceHash.Compute(
                index,
                atUtc,
                "run_closed",
                payloadJson,
                previousSha);
            lines[^1] = JsonSerializer.Serialize(
                new
                {
                    index,
                    atUtc,
                    monotonicTicks,
                    kind = "run_closed",
                    payload = payloadDocument.RootElement.Clone(),
                    previousSha256 = previousSha,
                    sha256 = replacementHash
                });
            File.WriteAllLines(evidencePath, lines);

            var result = EvidenceVerifier.VerifyBundle(
                runDirectory,
                requireClosed: true);

            Assert.False(result.IsValid);
            Assert.Equal("RUN_CLOSE_COUNT_MISMATCH", result.Error);
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }

    [Fact]
    public void EvidenceRejectsStructurallyIncompleteManifest()
    {
        var root = Path.Combine(
            Path.GetTempPath(),
            $"australis-ground-invalid-{Guid.NewGuid():N}");
        Directory.CreateDirectory(root);
        try
        {
            File.WriteAllText(Path.Combine(root, "manifest.json"), "{}");
            File.WriteAllText(Path.Combine(root, "evidence.jsonl"), "{}");

            var result = EvidenceVerifier.VerifyBundle(
                root,
                requireClosed: true);

            Assert.False(result.IsValid);
            Assert.StartsWith("MANIFEST:", result.Error);
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }

    [Fact]
    public void ControlTokenRejectsMissingOrWrongValues()
    {
        var token = new ControlRequestToken();

        Assert.False(token.Validate(null));
        Assert.False(token.Validate("wrong"));
        Assert.True(token.Validate(token.Value));
    }

    private static TelemetrySample Sample(
        long bootId,
        long seq,
        long tMs,
        int qualityFlags = 3) =>
        new(
            4,
            bootId,
            seq,
            tMs,
            1,
            qualityFlags,
            10,
            0,
            0,
            16384,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            DateTime.UtcNow,
            Stopwatch.GetTimestamp(),
            "HOST_UTC_UNVERIFIED");

    private static string Sha256File(string path) =>
        Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)))
            .ToLowerInvariant();

    private sealed class TestHostEnvironment : IHostEnvironment
    {
        public TestHostEnvironment(string root)
        {
            ContentRootPath = root;
            ContentRootFileProvider = new PhysicalFileProvider(root);
        }

        public string EnvironmentName { get; set; } = Environments.Development;
        public string ApplicationName { get; set; } =
            "GroundTelemetryDashboard.Tests";
        public string ContentRootPath { get; set; }
        public IFileProvider ContentRootFileProvider { get; set; }
    }
}
