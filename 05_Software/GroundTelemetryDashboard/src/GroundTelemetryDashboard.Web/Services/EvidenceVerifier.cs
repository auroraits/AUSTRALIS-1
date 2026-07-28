using System.Security.Cryptography;
using System.Text.Json;

namespace GroundTelemetryDashboard.Web.Services;

public sealed record EvidenceVerificationResult(
    bool IsValid,
    long RecordCount,
    string State,
    string? Error,
    string? FinalSha256);

public static class EvidenceVerifier
{
    public static EvidenceVerificationResult VerifyFile(string path) =>
        VerifyChain(path, null, null);

    public static EvidenceVerificationResult VerifyBundle(
        string runDirectory,
        bool requireClosed)
    {
        var manifestPath = Path.Combine(runDirectory, "manifest.json");
        var evidencePath = Path.Combine(runDirectory, "evidence.jsonl");
        if (!File.Exists(manifestPath) || !File.Exists(evidencePath))
        {
            return new(false, 0, "INVALID", "BUNDLE_FILES_MISSING", null);
        }

        string runId;
        string evidenceClass;
        string configurationSha256;
        string configurationFile;
        try
        {
            using var manifest = JsonDocument.Parse(
                File.ReadAllText(manifestPath));
            runId = manifest.RootElement.GetProperty("run_id").GetString() ?? "";
            evidenceClass =
                manifest.RootElement.GetProperty("evidence_class").GetString() ?? "";
            configurationSha256 = manifest.RootElement
                .GetProperty("configuration_sha256").GetString() ?? "";
            configurationFile = manifest.RootElement
                .GetProperty("configuration_file").GetString() ?? "";
        }
        catch (Exception ex) when (
            ex is JsonException or
            InvalidOperationException or
            KeyNotFoundException)
        {
            return new(false, 0, "INVALID", $"MANIFEST:{ex.Message}", null);
        }

        var manifestSha256 = Sha256(File.ReadAllBytes(manifestPath));
        var configurationPath = Path.Combine(runDirectory, configurationFile);
        if (!File.Exists(configurationPath) ||
            Sha256(File.ReadAllBytes(configurationPath)) != configurationSha256)
        {
            return new(
                false,
                0,
                "INVALID",
                "CONFIGURATION_SNAPSHOT_MISMATCH",
                null);
        }
        var chain = VerifyChain(evidencePath, runId, manifestSha256);
        if (!chain.IsValid)
        {
            return chain;
        }

        var sealPath = Path.Combine(runDirectory, "bundle_seal.json");
        if (!File.Exists(sealPath))
        {
            return requireClosed
                ? new(
                    false,
                    chain.RecordCount,
                    "ACTIVE_OR_TRUNCATED",
                    "RUN_NOT_CLOSED",
                    chain.FinalSha256)
                : chain with { State = "ACTIVE_PREFIX_VALID" };
        }
        if (chain.State != "CLOSED_CHAIN_VALID")
        {
            return new(
                false,
                chain.RecordCount,
                "INVALID",
                "RUN_CLOSE_MISSING",
                chain.FinalSha256);
        }

        try
        {
            using var seal = JsonDocument.Parse(File.ReadAllText(sealPath));
            var root = seal.RootElement;
            if (root.GetProperty("run_id").GetString() != runId ||
                root.GetProperty("record_count").GetInt64() != chain.RecordCount ||
                root.GetProperty("final_record_sha256").GetString() !=
                    chain.FinalSha256 ||
                root.GetProperty("manifest_sha256").GetString() !=
                    manifestSha256 ||
                root.GetProperty("evidence_file_sha256").GetString() !=
                    Sha256(File.ReadAllBytes(evidencePath)))
            {
                return new(
                    false,
                    chain.RecordCount,
                    "INVALID",
                    "SEAL_MISMATCH",
                    chain.FinalSha256);
            }
        }
        catch (Exception ex) when (
            ex is JsonException or InvalidOperationException or KeyNotFoundException)
        {
            return new(
                false,
                chain.RecordCount,
                "INVALID",
                $"SEAL:{ex.Message}",
                chain.FinalSha256);
        }

        if (evidenceClass != "CHAINED_BENCH_EVIDENCE")
        {
            return new(
                false,
                chain.RecordCount,
                "DIAGNOSTIC_ONLY",
                "UNIDENTIFIED_SOURCE_COMMIT",
                chain.FinalSha256);
        }

        return chain with { State = "COMPLETE_LOCAL_SEAL_VALID" };
    }

    private static EvidenceVerificationResult VerifyChain(
        string path,
        string? expectedRunId,
        string? expectedManifestSha256)
    {
        var previousHash = new string('0', 64);
        var expectedIndex = 1L;
        string? firstKind = null;
        string? lastKind = null;
        JsonElement firstPayload = default;
        JsonElement lastPayload = default;

        using var stream = new FileStream(
            path,
            FileMode.Open,
            FileAccess.Read,
            FileShare.ReadWrite);
        using var reader = new StreamReader(stream);
        string? line;
        while ((line = reader.ReadLine()) is not null)
        {
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            try
            {
                using var document = JsonDocument.Parse(line);
                var root = document.RootElement;
                var index = root.GetProperty("index").GetInt64();
                var atUtc = root.GetProperty("atUtc").GetDateTime();
                var kind = root.GetProperty("kind").GetString() ?? "";
                var payload = root.GetProperty("payload");
                var payloadJson = payload.GetRawText();
                var declaredPrevious =
                    root.GetProperty("previousSha256").GetString() ?? "";
                var declaredHash = root.GetProperty("sha256").GetString() ?? "";

                if (index != expectedIndex)
                {
                    return new(
                        false,
                        expectedIndex - 1,
                        "INVALID",
                        $"INDEX:{index}",
                        previousHash);
                }
                if (!string.Equals(
                        declaredPrevious,
                        previousHash,
                        StringComparison.Ordinal))
                {
                    return new(
                        false,
                        expectedIndex - 1,
                        "INVALID",
                        $"PREVIOUS_HASH:{index}",
                        previousHash);
                }

                var computed = EvidenceHash.Compute(
                    index,
                    atUtc,
                    kind,
                    payloadJson,
                    previousHash);
                if (!string.Equals(
                        declaredHash,
                        computed,
                        StringComparison.Ordinal))
                {
                    return new(
                        false,
                        expectedIndex - 1,
                        "INVALID",
                        $"HASH:{index}",
                        previousHash);
                }

                if (expectedIndex == 1)
                {
                    firstKind = kind;
                    firstPayload = payload.Clone();
                }
                lastKind = kind;
                lastPayload = payload.Clone();
                previousHash = computed;
                expectedIndex++;
            }
            catch (Exception ex) when (
                ex is JsonException or
                InvalidOperationException or
                KeyNotFoundException or
                FormatException)
            {
                return new(
                    false,
                    expectedIndex - 1,
                    "INVALID",
                    $"PARSE:{ex.Message}",
                    previousHash);
            }
        }

        var count = expectedIndex - 1;
        if (count == 0)
        {
            return new(false, 0, "INVALID", "EMPTY_CHAIN", null);
        }
        if (firstKind != "run_started")
        {
            return new(false, count, "INVALID", "RUN_START_MISSING", previousHash);
        }
        if (expectedRunId is not null &&
            (!firstPayload.TryGetProperty("run_id", out var firstRunId) ||
             !firstPayload.TryGetProperty(
                 "manifest_sha256",
                 out var firstManifestSha) ||
             firstRunId.GetString() != expectedRunId ||
             firstManifestSha.GetString() != expectedManifestSha256))
        {
            return new(
                false,
                count,
                "INVALID",
                "MANIFEST_ANCHOR_MISMATCH",
                previousHash);
        }
        if (lastKind == "run_closed")
        {
            if (expectedRunId is not null &&
                (!lastPayload.TryGetProperty("run_id", out var lastRunId) ||
                 lastRunId.GetString() != expectedRunId))
            {
                return new(
                    false,
                    count,
                    "INVALID",
                    "RUN_CLOSE_ID_MISMATCH",
                    previousHash);
            }
            if (!lastPayload.TryGetProperty(
                    "final_record_count",
                    out var finalRecordCount) ||
                finalRecordCount.ValueKind != JsonValueKind.Number ||
                !finalRecordCount.TryGetInt64(out var declaredRecordCount) ||
                declaredRecordCount != count)
            {
                return new(
                    false,
                    count,
                    "INVALID",
                    "RUN_CLOSE_COUNT_MISMATCH",
                    previousHash);
            }
        }

        return new(
            true,
            count,
            lastKind == "run_closed" ? "CLOSED_CHAIN_VALID" : "PREFIX_ONLY",
            null,
            previousHash);
    }

    private static string Sha256(byte[] value) =>
        Convert.ToHexString(SHA256.HashData(value)).ToLowerInvariant();
}
