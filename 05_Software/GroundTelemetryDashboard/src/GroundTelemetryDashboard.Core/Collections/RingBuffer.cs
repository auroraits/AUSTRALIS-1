namespace GroundTelemetryDashboard.Core.Collections;

public sealed class RingBuffer<T>
{
    private readonly T[] _items;
    private int _next;
    private int _count;
    private readonly object _sync = new();

    public RingBuffer(int capacity)
    {
        if (capacity <= 0) throw new ArgumentOutOfRangeException(nameof(capacity));
        _items = new T[capacity];
    }

    public void Add(T item)
    {
        lock (_sync)
        {
            _items[_next] = item;
            _next = (_next + 1) % _items.Length;
            if (_count < _items.Length) _count++;
        }
    }

    public IReadOnlyList<T> Snapshot()
    {
        lock (_sync)
        {
            var result = new List<T>(_count);
            var start = (_next - _count + _items.Length) % _items.Length;
            for (var i = 0; i < _count; i++)
            {
                result.Add(_items[(start + i) % _items.Length]);
            }
            return result;
        }
    }
}
