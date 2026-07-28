using GroundTelemetryDashboard.Core.Models;
using System.Diagnostics;

namespace GroundTelemetryDashboard.Core.Stats;

public sealed class StatsCalculator
{
    private readonly TimeSpan _window;
    private readonly Queue<WindowEvent> _windowEvents = new();
    private long _okTotal;
    private long _lostTotal;
    private long _duplicateTotal;
    private long _outOfOrderTotal;
    private long _timeRegressionTotal;
    private long _scientificAdmittedTotal;
    private long _scientificRejectedTotal;
    private long _sessionCount;
    private long? _lastSeq;
    private long? _lastTMs;
    private long? _currentBootId;
    private int? _currentProtocolVersion;

    public StatsCalculator(TimeSpan? window = null)
    {
        _window = window ?? TimeSpan.FromSeconds(30);
    }

    public TelemetryStats RegisterSample(TelemetrySample sample) =>
        RegisterSampleDetailed(sample).Stats;

    public TelemetryRegistration RegisterSampleDetailed(TelemetrySample sample)
    {
        var nowUtc = sample.ReceivedAtUtc;
        var nowTicks = sample.ReceivedMonotonicTicks;
        var received = 0L;
        var lost = 0L;
        var duplicate = 0L;
        var outOfOrder = 0L;
        var timeRegression = 0L;
        var scientificAdmitted = 0L;
        var scientificRejected = 0L;
        var linkDisposition = "RECEIVED";
        var scientificDisposition = "NOT_A_UNIQUE_LINK_FRAME";

        if (StartsNewSession(sample))
        {
            StartSession(sample);
        }

        if (!_lastSeq.HasValue)
        {
            received = 1;
            _lastSeq = sample.Seq;
            _lastTMs = sample.TMs;
            linkDisposition = "RECEIVED_SESSION_START";
        }
        else
        {
            var current = unchecked((uint)sample.Seq);
            var previous = unchecked((uint)_lastSeq.Value);
            var delta = unchecked(current - previous);
            if (delta == 0)
            {
                duplicate = 1;
                linkDisposition = "DUPLICATE";
            }
            else if (delta < 0x80000000U)
            {
                received = 1;
                lost = delta - 1;
                _lastSeq = sample.Seq;
                var currentTime = unchecked((uint)sample.TMs);
                var previousTime = unchecked((uint)_lastTMs!.Value);
                var timeDelta = unchecked(currentTime - previousTime);
                if (timeDelta == 0 || timeDelta >= 0x80000000U)
                {
                    timeRegression = 1;
                    linkDisposition = lost > 0
                        ? "RECEIVED_WITH_GAP"
                        : "RECEIVED";
                }
                else
                {
                    _lastTMs = sample.TMs;
                    linkDisposition = lost > 0
                        ? "RECEIVED_WITH_GAP"
                        : "RECEIVED";
                }
            }
            else
            {
                outOfOrder = 1;
                linkDisposition = "OUT_OF_ORDER";
            }
        }

        if (received == 1)
        {
            if (timeRegression == 1)
            {
                scientificRejected = 1;
                scientificDisposition = "TIME_REGRESSION";
            }
            else if (!sample.IsScientificQuality)
            {
                scientificRejected = 1;
                scientificDisposition = sample.ScientificValidationCode;
            }
            else
            {
                scientificAdmitted = 1;
                scientificDisposition = "ADMITTED";
            }
        }

        _okTotal += received;
        _lostTotal += lost;
        _duplicateTotal += duplicate;
        _outOfOrderTotal += outOfOrder;
        _timeRegressionTotal += timeRegression;
        _scientificAdmittedTotal += scientificAdmitted;
        _scientificRejectedTotal += scientificRejected;
        _windowEvents.Enqueue(new WindowEvent(
            nowTicks,
            received,
            lost,
            duplicate,
            outOfOrder,
            timeRegression,
            scientificAdmitted,
            scientificRejected));
        EvictOld(nowTicks);

        var receivedWindow = _windowEvents.Sum(e => e.Received);
        var lostWindow = _windowEvents.Sum(e => e.Lost);
        var duplicateWindow = _windowEvents.Sum(e => e.Duplicate);
        var outOfOrderWindow = _windowEvents.Sum(e => e.OutOfOrder);
        var timeRegressionWindow = _windowEvents.Sum(e => e.TimeRegression);
        var scientificAdmittedWindow =
            _windowEvents.Sum(e => e.ScientificAdmitted);
        var scientificRejectedWindow =
            _windowEvents.Sum(e => e.ScientificRejected);
        var linkDenominator = receivedWindow + lostWindow;
        double? linkSuccess = linkDenominator > 0
            ? (double)receivedWindow / linkDenominator
            : null;
        var scientificDenominator =
            scientificAdmittedWindow + scientificRejectedWindow;
        double? scientificYield = scientificDenominator > 0
            ? (double)scientificAdmittedWindow / scientificDenominator
            : null;

        var stats = new TelemetryStats(
            _okTotal,
            _lostTotal,
            _duplicateTotal,
            _outOfOrderTotal,
            _timeRegressionTotal,
            _sessionCount,
            receivedWindow,
            lostWindow,
            duplicateWindow,
            outOfOrderWindow,
            timeRegressionWindow,
            linkSuccess,
            linkSuccess.HasValue ? 1.0 - linkSuccess.Value : null,
            _scientificAdmittedTotal,
            _scientificRejectedTotal,
            scientificAdmittedWindow,
            scientificRejectedWindow,
            scientificYield,
            _lastSeq,
            _currentBootId,
            nowUtc);
        return new TelemetryRegistration(
            stats,
            linkDisposition,
            scientificDisposition,
            scientificAdmitted == 1);
    }

    private bool StartsNewSession(TelemetrySample sample)
    {
        if (!_currentProtocolVersion.HasValue)
        {
            return true;
        }
        if (sample.ProtocolVersion != _currentProtocolVersion.Value)
        {
            return true;
        }

        if (sample.ProtocolVersion >= 4)
        {
            return _currentProtocolVersion.Value < 4 || sample.BootId != _currentBootId;
        }

        if (_currentProtocolVersion.Value >= 4)
        {
            return true;
        }

        // Legacy packets have no boot ID. A simultaneous large time/counter
        // rollback is the explicit receiver-side reboot heuristic.
        return _lastTMs.HasValue &&
               _lastSeq.HasValue &&
               sample.TMs + 1000 < _lastTMs.Value &&
               sample.Seq + 16 < _lastSeq.Value;
    }

    private void StartSession(TelemetrySample sample)
    {
        _sessionCount++;
        _currentProtocolVersion = sample.ProtocolVersion;
        _currentBootId = sample.BootId;
        _lastSeq = null;
        _lastTMs = null;
        _windowEvents.Clear();
    }

    private void EvictOld(long nowTicks)
    {
        while (_windowEvents.Count > 0 &&
               Stopwatch.GetElapsedTime(
                   _windowEvents.Peek().AtMonotonicTicks,
                   nowTicks) > _window)
        {
            _windowEvents.Dequeue();
        }
    }

    private sealed record WindowEvent(
        long AtMonotonicTicks,
        long Received,
        long Lost,
        long Duplicate,
        long OutOfOrder,
        long TimeRegression,
        long ScientificAdmitted,
        long ScientificRejected);
}
