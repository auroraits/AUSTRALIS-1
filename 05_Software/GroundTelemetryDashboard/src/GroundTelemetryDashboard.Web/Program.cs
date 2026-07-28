using System.IO.Ports;
using System.Net;
using GroundTelemetryDashboard.Web.Hubs;
using GroundTelemetryDashboard.Web.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSignalR();
builder.Services.AddScoped(sp =>
{
    var nav = sp.GetRequiredService<Microsoft.AspNetCore.Components.NavigationManager>();
    return new HttpClient { BaseAddress = new Uri(nav.BaseUri) };
});
builder.Services.AddSingleton<TelemetryState>();
builder.Services.AddSingleton<EvidenceRecorder>();
builder.Services.AddSingleton<SerialConnectionManager>();
builder.Services.AddHostedService<SerialTelemetryHostedService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}

app.Use(async (context, next) =>
{
    var remoteAddress = context.Connection.RemoteIpAddress;
    if (remoteAddress is null || !IPAddress.IsLoopback(remoteAddress))
    {
        context.Response.StatusCode = StatusCodes.Status403Forbidden;
        await context.Response.WriteAsync(
            "GroundTelemetryDashboard is local-only. " +
            "Use a separately reviewed authenticated gateway for remote access.");
        return;
    }

    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("Referrer-Policy", "no-referrer");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    await next();
});

app.UseStaticFiles();
app.UseRouting();

app.MapGet("/api/ports", () => SerialPort.GetPortNames().OrderBy(x => x));
app.MapGet("/api/status", (SerialConnectionManager manager) => manager.GetStatus());
app.MapGet("/api/evidence/status", (EvidenceRecorder evidence) =>
{
    var evidenceFile = evidence.RunDirectory is null
        ? null
        : Path.Combine(evidence.RunDirectory, "evidence.jsonl");
    var verification = evidenceFile is not null && File.Exists(evidenceFile)
        ? EvidenceVerifier.VerifyFile(evidenceFile)
        : new EvidenceVerificationResult(false, 0, "EVIDENCE_DISABLED_OR_MISSING");
    return Results.Ok(new
    {
        evidence.Enabled,
        evidence.RunId,
        evidence.RunDirectory,
        verification
    });
});
app.MapPost("/api/connect", (
    ConnectRequest request,
    SerialConnectionManager manager,
    EvidenceRecorder evidence) =>
{
    var knownPorts = SerialPort.GetPortNames();
    if (!knownPorts.Contains(
            request.PortName,
            StringComparer.OrdinalIgnoreCase))
    {
        return Results.BadRequest(new
        {
            error = "UNKNOWN_SERIAL_PORT",
            known_ports = knownPorts.OrderBy(x => x)
        });
    }

    try
    {
        var status = manager.Connect(request.PortName, request.Baud);
        evidence.RecordConnection(status, "requested_connect");
        return Results.Ok(status);
    }
    catch (ArgumentException ex)
    {
        return Results.BadRequest(new { error = "INVALID_CONNECT_REQUEST", ex.Message });
    }
});
app.MapPost("/api/disconnect", (
    SerialConnectionManager manager,
    EvidenceRecorder evidence) =>
{
    manager.Disconnect();
    var status = manager.GetStatus();
    evidence.RecordConnection(status, "requested_disconnect");
    return Results.Ok(status);
});

app.MapBlazorHub();
app.MapHub<TelemetryHub>("/hubs/telemetry");
app.MapFallbackToPage("/_Host");

app.Run();

internal sealed record ConnectRequest(string PortName, int? Baud);
