using System.Security.Cryptography;
using System.Text;

namespace GroundTelemetryDashboard.Web.Services;

public sealed class ControlRequestToken
{
    private readonly string _value =
        Convert.ToHexString(RandomNumberGenerator.GetBytes(32))
            .ToLowerInvariant();

    public string Value => _value;

    public bool Validate(string? candidate)
    {
        if (candidate is null)
        {
            return false;
        }
        var expected = Encoding.UTF8.GetBytes(_value);
        var actual = Encoding.UTF8.GetBytes(candidate);
        return expected.Length == actual.Length &&
               CryptographicOperations.FixedTimeEquals(expected, actual);
    }
}
