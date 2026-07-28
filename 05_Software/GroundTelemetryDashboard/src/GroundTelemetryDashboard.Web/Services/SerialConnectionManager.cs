namespace GroundTelemetryDashboard.Web.Services;

public sealed class SerialConnectionManager
{
    private readonly object _sync = new();
    private string? _portName;
    private int _baud;
    private bool _connected;
    private long _generation;

    public SerialConnectionManager(IConfiguration configuration)
    {
        _baud = configuration.GetValue<int?>("Serial:BaudRate") ?? 115200;
    }

    public ConnectionStatus Connect(string portName, int? baud)
    {
        if (string.IsNullOrWhiteSpace(portName))
        {
            throw new ArgumentException("Port name is required.", nameof(portName));
        }

        var requestedBaud = baud ?? _baud;
        if (requestedBaud is < 1200 or > 2_000_000)
        {
            throw new ArgumentOutOfRangeException(nameof(baud));
        }

        lock (_sync)
        {
            _portName = portName.Trim();
            _baud = requestedBaud;
            _connected = true;
            _generation++;
            return Snapshot();
        }
    }

    public bool Disconnect(long? expectedGeneration = null)
    {
        lock (_sync)
        {
            if (expectedGeneration.HasValue &&
                expectedGeneration.Value != _generation)
            {
                return false;
            }

            _connected = false;
            _generation++;
            return true;
        }
    }

    public ConnectionStatus GetStatus()
    {
        lock (_sync)
        {
            return Snapshot();
        }
    }

    private ConnectionStatus Snapshot() =>
        new(_connected, _portName, _baud, _generation);
}
