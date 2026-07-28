using System.Text.Json;

namespace GroundTelemetryDashboard.Web.Services;

public sealed record EvidenceVerificationResult(
    bool IsValid,
    long RecordCount,
    string? Error);

public static class EvidenceVerifier
{
    public static EvidenceVerificationResult VerifyFile(string path)
    {
        var previousHash = new string('0', 64);
        var expectedIndex = 1L;

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
                var payloadJson = root.GetProperty("payload").GetRawText();
                var declaredPrevious =
                    root.GetProperty("previousSha256").GetString() ?? "";
                var declaredHash = root.GetProperty("sha256").GetString() ?? "";

                if (index != expectedIndex)
                {
                    return new(false, expectedIndex - 1, $"INDEX:{index}");
                }
                if (!string.Equals(
                        declaredPrevious,
                        previousHash,
                        StringComparison.Ordinal))
                {
                    return new(false, expectedIndex - 1, $"PREVIOUS_HASH:{index}");
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
                    return new(false, expectedIndex - 1, $"HASH:{index}");
                }

                previousHash = computed;
                expectedIndex++;
            }
            catch (Exception ex) when (
                ex is JsonException or
                InvalidOperationException or
                KeyNotFoundException or
                FormatException)
            {
                return new(false, expectedIndex - 1, $"PARSE:{ex.Message}");
            }
        }

        return new(true, expectedIndex - 1, null);
    }
}
