using System.Globalization;
using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Core.Parsing;

public static class SerialLineParser
{
    public static bool TryParseCsvLine(string line, out TelemetrySample? sample)
    {
        sample = null;
        if (string.IsNullOrWhiteSpace(line)) return false;

        var parts = line.Trim().Split(',', StringSplitOptions.TrimEntries);
        if (parts.Length is not (8 or 12)) return false;

        if (!long.TryParse(parts[0], NumberStyles.Integer, CultureInfo.InvariantCulture, out var seq) ||
            !long.TryParse(parts[1], NumberStyles.Integer, CultureInfo.InvariantCulture, out var tMs) ||
            !double.TryParse(parts[2], NumberStyles.Float, CultureInfo.InvariantCulture, out var ax) ||
            !double.TryParse(parts[3], NumberStyles.Float, CultureInfo.InvariantCulture, out var ay) ||
            !double.TryParse(parts[4], NumberStyles.Float, CultureInfo.InvariantCulture, out var az) ||
            !double.TryParse(parts[5], NumberStyles.Float, CultureInfo.InvariantCulture, out var gx) ||
            !double.TryParse(parts[6], NumberStyles.Float, CultureInfo.InvariantCulture, out var gy) ||
            !double.TryParse(parts[7], NumberStyles.Float, CultureInfo.InvariantCulture, out var gz))
        {
            return false;
        }

        var q0 = 1.0;
        var q1 = 0.0;
        var q2 = 0.0;
        var q3 = 0.0;

        if (parts.Length == 12 &&
            (!double.TryParse(parts[8], NumberStyles.Float, CultureInfo.InvariantCulture, out q0) ||
             !double.TryParse(parts[9], NumberStyles.Float, CultureInfo.InvariantCulture, out q1) ||
             !double.TryParse(parts[10], NumberStyles.Float, CultureInfo.InvariantCulture, out q2) ||
             !double.TryParse(parts[11], NumberStyles.Float, CultureInfo.InvariantCulture, out q3)))
        {
            return false;
        }

        sample = new TelemetrySample(seq, tMs, ax, ay, az, gx, gy, gz, q0, q1, q2, q3, DateTime.UtcNow);
        return true;
    }
}
