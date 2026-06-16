# GroundTelemetryDashboard

Dashboard de telemetría de estación terrena (Arduino UNO por serial COM) implementado con .NET 8 + Blazor Server + SignalR.

## Requisitos
- .NET SDK 8.x

## Cómo correr
```bash
dotnet restore 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln
dotnet build 05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln
dotnet run --project 05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web
```

### Acceso desde red local (LAN)
Para exponer el dashboard en toda la red local (sin restringir a `localhost`), correr:
```bash
ASPNETCORE_URLS="http://0.0.0.0:3000" dotnet run --project 05_Software/GroundTelemetryDashboard/src/GroundTelemetryDashboard.Web
```
Luego abrir desde otro equipo: `http://<LAN-IP>:3000`.

Notas:
- Para obtener tu IP local (Windows): `ipconfig`.
- Exponer en LAN solo en una red confiable.

## CSV soportado
- Legacy: `seq,t_ms,ax,ay,az,gx,gy,gz`
- Quaternion: `seq,t_ms,ax,ay,az,gx,gy,gz,q0,q1,q2,q3`

`q0..q3 = qw,qx,qy,qz`.

## Vista 3D
- Aplicación de quaternion correcta para Three.js:
  - `obj.quaternion.set(qx,qy,qz,qw)`
- Zero visual:
  - botón **Set Reference (Zero)**
  - fórmula: `q_display = inverse(q_ref) * q_current`
- Camera:
  - OrbitControls habilitado
  - modo **Follow ON/OFF**
- HUD:
  - roll/pitch/yaw visual para diagnóstico

## Debug de ejes
- Botón **Axis Debug** agrega líneas `#AXIS` al terminal con `ax..gz` y `q`.
- Útil para verificar signos por eje al mover el módulo.

## Nota IMU
- Sensor objetivo: GY-521 (MPU6050).
- El TX reporta por Serial: `#SENSOR:MPU6050 addr=0x68|0x69`.
