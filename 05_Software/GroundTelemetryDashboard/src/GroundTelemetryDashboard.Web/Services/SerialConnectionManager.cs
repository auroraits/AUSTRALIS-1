namespace GroundTelemetryDashboard.Web.Services;

public sealed class SerialConnectionManager
{
    private readonly IConfiguration _configuration;
    private readonly object _sync = new();
    private string? _portName;
    private int _baud;
    private bool _connected;

    public SerialConnectionManager(IConfiguration configuration)
    {
        _configuration = configuration;
        _baud = _configuration.GetValue<int?>("Serial:BaudRate") ?? 115200;
    }

    public void Connect(string portName, int? baud)
    {
        lock (_sync)
        {
            _portName = portName;
            _baud = baud ?? _baud;
            _connected = true;
        }
    }

    public void Disconnect()
    {
        lock (_sync)
        {
            _connected = false;
        }
    }

    public ConnectionStatus GetStatus()
    {
        lock (_sync)
        {
            return new ConnectionStatus(_connected, _portName, _baud);
        }
    }
}
