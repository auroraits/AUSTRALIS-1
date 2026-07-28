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
            "4,305419896,7,1200,3,100,-100,16384,5,-6,7,1,0,0,0";

        var ok = SerialLineParser.TryParseCsvLine(
            line,
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.Equal(4, sample.ProtocolVersion);
        Assert.Equal(305419896, sample.BootId);
        Assert.Equal(7, sample.Seq);
        Assert.Equal(3, sample.QualityFlags);
        Assert.Equal("v4-12345678", sample.SessionId);
    }

    [Theory]
    [InlineData("4,1,1,1,1,NaN,0,0,0,0,0,1,0,0,0", "NONFINITE_OR_INVALID_NUMBER")]
    [InlineData("4,1,1,1,1,40000,0,0,0,0,0,1,0,0,0", "SENSOR_RANGE")]
    [InlineData("4,1,1,1,1,0,0,0,0,0,0,2,0,0,0", "QUATERNION_NORM")]
    [InlineData("5,1,1,1,1,0,0,0,0,0,0,1,0,0,0", "V4_HEADER")]
    public void ParserRejectsInvalidScientificData(
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

    [Fact]
    public void ParserRetainsLegacyCompatibility()
    {
        var ok = SerialLineParser.TryParseCsvLine(
            "7,1200,100,-100,16384,5,-6,7",
            out var sample,
            out var error);

        Assert.True(ok, error);
        Assert.NotNull(sample);
        Assert.Equal(1, sample.ProtocolVersion);
        Assert.Equal(1, sample.Q0);
    }

    [Fact]
    public void StatsDoNotCountRebootAsPacketLoss()
    {
        var calculator = new StatsCalculator(TimeSpan.FromMinutes(1));
        calculator.RegisterSample(Sample(100, 10, 1000));
        calculator.RegisterSample(Sample(100, 13, 2500));
        var afterReboot = calculator.RegisterSample(Sample(200, 0, 20));

        Assert.Equal(2, afterReboot.LostCountEstimated);
        Assert.Equal(2, afterReboot.SessionCount);
        Assert.Equal(0, afterReboot.LostCountWindow);
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

        Assert.Equal(0, stats.LostCountEstimated);
        Assert.Equal(1, stats.DuplicateCount);
        Assert.Equal(1, stats.OutOfOrderCount);
        Assert.Equal(0, stats.LastSeq);
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
        Assert.True(manager.GetStatus().IsConnected);
        Assert.True(manager.Disconnect(second.Generation));
    }

    [Fact]
    public void EvidenceIsPersistentAndTamperEvident()
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
                    ["Evidence:Root"] = root
                })
                .Build();
            var environment = new TestHostEnvironment(root);
            string evidenceFile;

            using (var recorder = new EvidenceRecorder(
                       configuration,
                       environment,
                       NullLogger<EvidenceRecorder>.Instance))
            {
                recorder.RecordRawLine("línea de diagnóstico, ñ");
                recorder.RecordSample(Sample(1, 1, 1));
                evidenceFile = Path.Combine(
                    recorder.RunDirectory!,
                    "evidence.jsonl");
            }

            var valid = EvidenceVerifier.VerifyFile(evidenceFile);
            Assert.True(valid.IsValid, valid.Error);
            Assert.Equal(4, valid.RecordCount);

            var content = File.ReadAllText(evidenceFile);
            File.WriteAllText(
                evidenceFile,
                content.Replace(
                    "raw_serial_line",
                    "tampered_serial_line",
                    StringComparison.Ordinal));
            var tampered = EvidenceVerifier.VerifyFile(evidenceFile);
            Assert.False(tampered.IsValid);
            Assert.StartsWith("HASH:", tampered.Error);
        }
        finally
        {
            Directory.Delete(root, recursive: true);
        }
    }

    private static TelemetrySample Sample(
        long bootId,
        long seq,
        long tMs) =>
        new(
            4,
            bootId,
            seq,
            tMs,
            3,
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
            DateTime.UtcNow);

    private sealed class TestHostEnvironment : IHostEnvironment
    {
        public TestHostEnvironment(string root)
        {
            ContentRootPath = root;
            ContentRootFileProvider = new PhysicalFileProvider(root);
        }

        public string EnvironmentName { get; set; } = Environments.Development;
        public string ApplicationName { get; set; } = "GroundTelemetryDashboard.Tests";
        public string ContentRootPath { get; set; }
        public IFileProvider ContentRootFileProvider { get; set; }
    }
}
