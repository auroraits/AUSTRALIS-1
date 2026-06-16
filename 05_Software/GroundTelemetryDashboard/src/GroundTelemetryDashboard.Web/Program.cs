using System.IO.Ports;
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
builder.Services.AddSingleton<SerialConnectionManager>();
builder.Services.AddHostedService<SerialTelemetryHostedService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}

app.UseStaticFiles();
app.UseRouting();

app.MapGet("/api/ports", () => SerialPort.GetPortNames().OrderBy(x => x));
app.MapGet("/api/status", (SerialConnectionManager manager) => manager.GetStatus());
app.MapPost("/api/connect", (ConnectRequest request, SerialConnectionManager manager) =>
{
    manager.Connect(request.PortName, request.Baud);
    return Results.Ok(manager.GetStatus());
});
app.MapPost("/api/disconnect", (SerialConnectionManager manager) =>
{
    manager.Disconnect();
    return Results.Ok(manager.GetStatus());
});

app.MapBlazorHub();
app.MapHub<TelemetryHub>("/hubs/telemetry");
app.MapFallbackToPage("/_Host");

app.Run();

internal sealed record ConnectRequest(string PortName, int? Baud);
