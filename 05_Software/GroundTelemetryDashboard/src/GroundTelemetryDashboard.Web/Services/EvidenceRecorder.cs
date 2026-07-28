using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class EvidenceRecorder : IDisposable
{
    private readonly object _sync = new();
    private readonly StreamWriter? _writer;
    private readonly JsonSerializerOptions _jsonOptions =
        new(JsonSerializerDefaults.Web);
    private string _previousHash = new('0', 64);
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

        var configuredRoot =
            configuration.GetValue<string>("Evidence:Root") ?? "evidence";
        var root = Path.IsPathRooted(configuredRoot)
            ? configuredRoot
            : Path.Combine(environment.ContentRootPath, configuredRoot);
        RunDirectory = Path.GetFullPath(Path.Combine(root, RunId));
        Directory.CreateDirectory(RunDirectory);

        var manifest = new
        {
            schema_version = "AUSTRALIS_GROUND_EVIDENCE_V1",
            run_id = RunId,
            started_at_utc = DateTime.UtcNow,
            host = Environment.MachineName,
            os = Environment.OSVersion.ToString(),
            process_architecture =
                System.Runtime.InteropServices.RuntimeInformation.ProcessArchitecture.ToString(),
            application_version =
                typeof(EvidenceRecorder).Assembly.GetName().Version?.ToString(),
            source_commit = Environment.GetEnvironmentVariable("AUSTRALIS_SOURCE_COMMIT"),
            chain_algorithm = "SHA-256(index\\nat_utc_O\\nkind\\nprevious_sha256\\npayload_json)",
            evidence_file = "evidence.jsonl"
        };
        File.WriteAllText(
            Path.Combine(RunDirectory, "manifest.json"),
            JsonSerializer.Serialize(manifest, _jsonOptions),
            Encoding.UTF8);

        var stream = new FileStream(
            Path.Combine(RunDirectory, "evidence.jsonl"),
            FileMode.Append,
            FileAccess.Write,
            FileShare.Read);
        _writer = new StreamWriter(stream, new UTF8Encoding(false))
        {
            AutoFlush = true
        };
        Record("run_started", new { run_id = RunId });
        logger.LogInformation(
            "Ground evidence recording started at {RunDirectory}",
            RunDirectory);
    }

    public bool Enabled { get; }

    public string RunId { get; }

    public string? RunDirectory { get; }

    public void RecordRawLine(string line) =>
        Record("raw_serial_line", new { line });

    public void RecordSample(TelemetrySample sample) =>
        Record("validated_sample", sample);

    public void RecordRejectedLine(string line, string reasonCode) =>
        Record("rejected_serial_line", new { reason_code = reasonCode, line });

    public void RecordConnection(ConnectionStatus status, string action) =>
        Record("serial_connection", new { action, status });

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

            var index = ++_recordIndex;
            var atUtc = DateTime.UtcNow;
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
                kind,
                payloadElement,
                _previousHash,
                hash);
            _writer.WriteLine(JsonSerializer.Serialize(complete, _jsonOptions));
            _previousHash = hash;
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

            if (_writer is not null)
            {
                var index = ++_recordIndex;
                var atUtc = DateTime.UtcNow;
                var payloadJson = JsonSerializer.Serialize(
                    new { run_id = RunId },
                    _jsonOptions);
                using var payloadDocument = JsonDocument.Parse(payloadJson);
                var payloadElement = payloadDocument.RootElement.Clone();
                var hash = EvidenceHash.Compute(
                    index,
                    atUtc,
                    "run_closed",
                    payloadJson,
                    _previousHash);
                _writer.WriteLine(JsonSerializer.Serialize(
                    new EvidenceRecord(
                        index,
                        atUtc,
                        "run_closed",
                        payloadElement,
                        _previousHash,
                        hash),
                    _jsonOptions));
                _writer.Dispose();
            }

            _disposed = true;
        }
    }

    private sealed record EvidenceRecord(
        long Index,
        DateTime AtUtc,
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
