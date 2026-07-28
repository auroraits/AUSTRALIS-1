using System.Globalization;
using GroundTelemetryDashboard.Core.Models;

namespace GroundTelemetryDashboard.Core.Parsing;

public static class SerialLineParser
{
    private const double QuaternionNormMinSquared = 0.81;
    private const double QuaternionNormMaxSquared = 1.21;

    public static bool TryParseCsvLine(string line, out TelemetrySample? sample) =>
        TryParseCsvLine(line, out sample, out _);

    public static bool TryParseCsvLine(
        string line,
        out TelemetrySample? sample,
        out string? errorCode)
    {
        sample = null;
        errorCode = null;
        if (string.IsNullOrWhiteSpace(line))
        {
            errorCode = "EMPTY";
            return false;
        }

        var parts = line.Trim().Split(',', StringSplitOptions.TrimEntries);
        if (parts.Length is not (8 or 12 or 15))
        {
            errorCode = "FIELD_COUNT";
            return false;
        }

        var protocolVersion = parts.Length == 8 ? 1 : parts.Length == 12 ? 3 : 0;
        var bootId = 0L;
        var qualityFlags = 0;
        var seqIndex = 0;
        var timeIndex = 1;
        var sensorStart = 2;

        if (parts.Length == 15)
        {
            if (!TryParseLong(parts[0], 4, 4, out var parsedVersion) ||
                !TryParseLong(parts[1], 0, uint.MaxValue, out bootId) ||
                !TryParseLong(parts[4], 0, byte.MaxValue, out var parsedFlags))
            {
                errorCode = "V4_HEADER";
                return false;
            }

            protocolVersion = (int)parsedVersion;
            qualityFlags = (int)parsedFlags;
            seqIndex = 2;
            timeIndex = 3;
            sensorStart = 5;
        }

        if (!TryParseLong(parts[seqIndex], 0, uint.MaxValue, out var seq) ||
            !TryParseLong(parts[timeIndex], 0, uint.MaxValue, out var tMs))
        {
            errorCode = "COUNTER";
            return false;
        }

        var values = new double[10];
        var sensorFieldCount = parts.Length == 8 ? 6 : 10;
        for (var index = 0; index < sensorFieldCount; index++)
        {
            if (!TryParseFiniteDouble(parts[sensorStart + index], out values[index]))
            {
                errorCode = "NONFINITE_OR_INVALID_NUMBER";
                return false;
            }
        }

        for (var index = 0; index < 6; index++)
        {
            if (values[index] < short.MinValue || values[index] > short.MaxValue)
            {
                errorCode = "SENSOR_RANGE";
                return false;
            }
        }

        if (parts.Length == 8)
        {
            values[6] = 1.0;
        }

        var normSquared =
            values[6] * values[6] +
            values[7] * values[7] +
            values[8] * values[8] +
            values[9] * values[9];
        if (normSquared < QuaternionNormMinSquared ||
            normSquared > QuaternionNormMaxSquared)
        {
            errorCode = "QUATERNION_NORM";
            return false;
        }

        sample = new TelemetrySample(
            protocolVersion,
            bootId,
            seq,
            tMs,
            qualityFlags,
            values[0],
            values[1],
            values[2],
            values[3],
            values[4],
            values[5],
            values[6],
            values[7],
            values[8],
            values[9],
            DateTime.UtcNow);
        return true;
    }

    private static bool TryParseLong(
        string value,
        long minimum,
        long maximum,
        out long result)
    {
        if (!long.TryParse(
                value,
                NumberStyles.Integer,
                CultureInfo.InvariantCulture,
                out result))
        {
            return false;
        }

        return result >= minimum && result <= maximum;
    }

    private static bool TryParseFiniteDouble(string value, out double result)
    {
        return double.TryParse(
                   value,
                   NumberStyles.Float,
                   CultureInfo.InvariantCulture,
                   out result) &&
               double.IsFinite(result);
    }
}
