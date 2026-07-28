using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class EvidenceRecorder : IDisposable
{
    private readonly object _sync = new();
    private readonly StreamWriter? _writer;
    private readonly JsonSerializerOptions _jsonOptions =
        new(JsonSerializerDefaults.Web);
    private readonly string? _manifestPath;
    private readonly string? _evidencePath;
    private readonly string? _manifestSha256;
    private readonly string? _sourceCommit;
    private string _previousHash = new('0', 64);
    private string? _acquisitionSessionId;
    private long _recordIndex;
    private bool _disposed;

    public EvidenceRecorder(
        IConfiguration configuration,
        IHostEnvironment environment,
        ILogger<EvidenceRecorder> logger)
    {
        Enabled = configuration.GetValue<bool?>("Evidence:Enabled") ?? true;
        RunId = $"ground-{DateTime.UtcNow:yyyyMMddTHHmmssZ}-{Guid.NewGuid():N}";
        if (!Enabled)
        {
            logger.LogWarning("Evidence recording is disabled by configuration.");
            return;
        }

        _sourceCommit = (
            configuration.GetValue<string>("Evidence:SourceCommit") ??
            Environment.GetEnvironmentVariable("AUSTRALIS_SOURCE_COMMIT") ??
            "").Trim();
        SourceIdentified = Regex.IsMatch(
            _sourceCommit,
            "^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$");
        EvidenceClass = SourceIdentified
            ? "CHAINED_BENCH_EVIDENCE"
            : "DIAGNOSTIC_ONLY_UNIDENTIFIED_SOURCE";

        var configuredRoot =
            configuration.GetValue<string>("Evidence:Root") ?? "evidence";
        var root = Path.IsPathRooted(configuredRoot)
            ? configuredRoot
            : Path.Combine(environment.ContentRootPath, configuredRoot);
        RunDirectory = Path.GetFullPath(Path.Combine(root, RunId));
        Directory.CreateDirectory(RunDirectory);

        var configurationSnapshot = configuration.AsEnumerable()
            .Where(item =>
                item.Value is not null &&
                (item.Key.StartsWith("Serial:", StringComparison.Ordinal) ||
                 item.Key.StartsWith("Evidence:", StringComparison.Ordinal)) &&
                !item.Key.EndsWith("SourceCommit", StringComparison.Ordinal))
            .OrderBy(item => item.Key, StringComparer.Ordinal)
            .ToDictionary(
                item => item.Key,
                item => item.Value,
                StringComparer.Ordinal);
        var configurationJson =
            JsonSerializer.Serialize(configurationSnapshot, _jsonOptions);
        File.WriteAllText(
            Path.Combine(RunDirectory, "configuration.json"),
            configurationJson,
            new UTF8Encoding(false));

        var manifest = new
        {
            schema_version = "AUSTRALIS_GROUND_EVIDENCE_V2",
            run_id = RunId,
            started_at_utc = DateTime.UtcNow,
            host = Environment.MachineName,
            os = Environment.OSVersion.ToString(),
            process_architecture =
                System.Runtime.InteropServices.RuntimeInformation
                    .ProcessArchitecture.ToString(),
            application_version =
                typeof(EvidenceRecorder).Assembly.GetName().Version?.ToString(),
            source_commit_claim = SourceIdentified ? _sourceCommit : null,
            source_commit_verification =
                "CLAIM_ONLY_NOT_REPOSITORY_RESOLVED",
            evidence_class = EvidenceClass,
            configuration_sha256 = Sha256(configurationJson),
            configuration_file = "configuration.json",
            utc_time_quality = "HOST_UTC_UNVERIFIED",
            monotonic_time_source = "System.Diagnostics.Stopwatch",
            chain_algorithm =
                "SHA-256(index\\nat_utc_O\\nkind\\nprevious_sha256\\npayload_json)",
            evidence_file = "evidence.jsonl",
            seal_file = "bundle_seal.json",
            external_anchor_status = "OPEN"
        };
        _manifestPath = Path.Combine(RunDirectory, "manifest.json");
        File.WriteAllText(
            _manifestPath,
            JsonSerializer.Serialize(manifest, _jsonOptions),
            new UTF8Encoding(false));
        _manifestSha256 = Sha256(File.ReadAllBytes(_manifestPath));

        _evidencePath = Path.Combine(RunDirectory, "evidence.jsonl");
        var stream = new FileStream(
            _evidencePath,
            FileMode.CreateNew,
            FileAccess.Write,
            FileShare.Read);
        _writer = new StreamWriter(stream, new UTF8Encoding(false))
        {
            AutoFlush = true
        };
        Record(
            "run_started",
            new
            {
                run_id = RunId,
                manifest_sha256 = _manifestSha256,
                evidence_class = EvidenceClass
            });
        logger.LogInformation(
            "Ground evidence recording started at {RunDirectory}; class={EvidenceClass}",
            RunDirectory,
            EvidenceClass);
        if (!SourceIdentified)
        {
            logger.LogWarning(
                "AUSTRALIS source commit is missing/invalid; bundle is diagnostic only.");
        }
    }

    public bool Enabled { get; }

    public bool SourceIdentified { get; }

    public string EvidenceClass { get; } = "DISABLED";

    public string RunId { get; }

    public string? RunDirectory { get; }

    public void RecordRawLine(string line) =>
        Record(
            "raw_serial_line",
            new { acquisition_session_id = _acquisitionSessionId, line });

    public void RecordSample(
        TelemetrySample sample,
        TelemetryRegistration registration) =>
        Record(
            "parsed_serial_sample",
            new
            {
                acquisition_session_id = _acquisitionSessionId,
                link_disposition = registration.LinkDisposition,
                scientific_disposition = registration.ScientificDisposition,
                accepted_for_series = registration.AcceptedForSeries,
                sensor_quality_valid = sample.IsScientificQuality,
                scientific_validation_code = sample.ScientificValidationCode,
                measurement_class = sample.MeasurementClass,
                sample
            });

    public void RecordRejectedLine(string line, string reasonCode) =>
        Record(
            "rejected_serial_line",
            new
            {
                acquisition_session_id = _acquisitionSessionId,
                reason_code = reasonCode,
                line
            });

    public void RecordConnection(ConnectionStatus status, string action)
    {
        if (action == "opened")
        {
            _acquisitionSessionId =
                $"serial-{status.Generation}-{Guid.NewGuid():N}";
        }
        Record(
            "serial_connection",
            new
            {
                action,
                acquisition_session_id = _acquisitionSessionId,
                status
            });
        if (action is "closed_or_reconfigured" or "serial_error")
        {
            _acquisitionSessionId = null;
        }
    }

    public void Record(string kind, object payload)
    {
        if (!Enabled || _writer is null)
        {
            return;
        }

        lock (_sync)
        {
            if (_disposed)
            {
                return;
            }
            RecordLocked(kind, payload);
        }
    }

    public void Dispose()
    {
        lock (_sync)
        {
            if (_disposed)
            {
                return;
            }

            if (_writer is not null &&
                _evidencePath is not null &&
                _manifestSha256 is not null &&
                RunDirectory is not null)
            {
                if (_acquisitionSessionId is not null)
                {
                    RecordLocked(
                        "serial_connection",
                        new
                        {
                            action = "closed_at_process_shutdown",
                            acquisition_session_id = _acquisitionSessionId
                        });
                    _acquisitionSessionId = null;
                }
                RecordLocked(
                    "run_closed",
                    new
                    {
                        run_id = RunId,
                        final_record_count = _recordIndex + 1
                    });
                _writer.Dispose();

                var seal = new
                {
                    schema_version = "AUSTRALIS_GROUND_EVIDENCE_SEAL_V1",
                    run_id = RunId,
                    closed_at_utc = DateTime.UtcNow,
                    record_count = _recordIndex,
                    final_record_sha256 = _previousHash,
                    manifest_sha256 = _manifestSha256,
                    evidence_file_sha256 = Sha256(File.ReadAllBytes(_evidencePath)),
                    source_commit_claim = SourceIdentified ? _sourceCommit : null,
                    source_commit_verification =
                        "CLAIM_ONLY_NOT_REPOSITORY_RESOLVED",
                    evidence_class = EvidenceClass,
                    external_anchor_status = "OPEN"
                };
                File.WriteAllText(
                    Path.Combine(RunDirectory, "bundle_seal.json"),
                    JsonSerializer.Serialize(seal, _jsonOptions),
                    new UTF8Encoding(false));
            }

            _disposed = true;
        }
    }

    private void RecordLocked(string kind, object payload)
    {
        var index = ++_recordIndex;
        var atUtc = DateTime.UtcNow;
        var monotonicTicks = System.Diagnostics.Stopwatch.GetTimestamp();
        var payloadJson = JsonSerializer.Serialize(payload, _jsonOptions);
        using var payloadDocument = JsonDocument.Parse(payloadJson);
        var payloadElement = payloadDocument.RootElement.Clone();
        var hash = EvidenceHash.Compute(
            index,
            atUtc,
            kind,
            payloadJson,
            _previousHash);
        var complete = new EvidenceRecord(
            index,
            atUtc,
            monotonicTicks,
            kind,
            payloadElement,
            _previousHash,
            hash);
        _writer!.WriteLine(JsonSerializer.Serialize(complete, _jsonOptions));
        _previousHash = hash;
    }

    private static string Sha256(string value) =>
        Sha256(Encoding.UTF8.GetBytes(value));

    private static string Sha256(byte[] value) =>
        Convert.ToHexString(SHA256.HashData(value)).ToLowerInvariant();

    private sealed record EvidenceRecord(
        long Index,
        DateTime AtUtc,
        long MonotonicTicks,
        string Kind,
        JsonElement Payload,
        string PreviousSha256,
        string Sha256);
}

public static class EvidenceHash
{
    public static string Compute(
        long index,
        DateTime atUtc,
        string kind,
        string payloadJson,
        string previousSha256)
    {
        var input = string.Join(
            "\n",
            index.ToString(System.Globalization.CultureInfo.InvariantCulture),
            atUtc.ToUniversalTime().ToString(
                "O",
                System.Globalization.CultureInfo.InvariantCulture),
            kind,
            previousSha256,
            payloadJson);
        return Convert.ToHexString(
                SHA256.HashData(Encoding.UTF8.GetBytes(input)))
            .ToLowerInvariant();
    }
}
