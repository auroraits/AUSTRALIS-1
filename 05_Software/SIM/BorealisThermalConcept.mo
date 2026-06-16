within ;
package BorealisThermalConcept
  import Modelica.Constants.pi;
  import Modelica.Constants.sigma;

  function deg2rad
    input Real deg;
    output Real rad;
  algorithm
    rad := deg*pi/180.0;
  end deg2rad;

  function posPart
    input Real x;
    output Real y;
  algorithm
    y := if x > 0 then x else 0;
  end posPart;

  model LEO500kmNadir_1p5U
    "Conceptual lumped-parameter thermal + solar model for a 1.5U nadir-pointing CubeSat"

    // -------------------------------------------------------------------------
    // Geometry convention
    // Face 1 = +X (ram)
    // Face 2 = -X (wake)
    // Face 3 = +Y
    // Face 4 = -Y
    // Face 5 = +Z (nadir, Earth-facing)
    // Face 6 = -Z (zenith, space-facing / preferred radiator face)
    // -------------------------------------------------------------------------
    parameter Real Lx = 0.10 "X dimension [m]";
    parameter Real Ly = 0.10 "Y dimension [m]";
    parameter Real Lz = 0.15 "Z dimension [m]";
    parameter Real A_face[6] = {Ly*Lz, Ly*Lz, Lx*Lz, Lx*Lz, Lx*Ly, Lx*Ly}
      "Areas of +X, -X, +Y, -Y, +Z(nadir), -Z(zenith) [m2]";
    parameter Real faceNormal[6,3] = [1,0,0; -1,0,0; 0,1,0; 0,-1,0; 0,0,1; 0,0,-1]
      "Body-fixed face normals";

    // -------------------------------------------------------------------------
    // Orbit / environment
    // -------------------------------------------------------------------------
    parameter Real alt = 500e3 "Orbital altitude [m]";
    parameter Real incl_deg = 98 "Inclination [deg] (informational in this simplified model)";
    parameter Real beta_deg = 0
      "Solar beta angle [deg]. 0 = stronger eclipse / thermal cycling. Change this for seasonal trade studies.";
    parameter Real RE = 6378.137e3 "Earth equatorial radius [m]";
    parameter Real mu = 3.986004418e14 "Earth gravitational parameter [m3/s2]";
    parameter Real solarFlux = 1361 "Solar constant [W/m2]";
    parameter Real earthIRFlux = 237 "Mean Earth IR flux seen from LEO [W/m2]";
    parameter Real albedo = 0.35 "Mean broadband Earth albedo factor";
    parameter Real Tspace = 3 "Deep-space sink temperature [K]";
    parameter Real phi0 = 0 "Initial orbital phase [rad]";
    final parameter Real a = RE + alt "Orbit radius [m]";
    final parameter Real n = sqrt(mu/a^3) "Orbital angular rate [rad/s]";
    final parameter Real Torbit = 2*pi/n "Orbital period [s]";
    final parameter Real beta = deg2rad(beta_deg) "Solar beta angle [rad]";

    // -------------------------------------------------------------------------
    // Surface optical properties
    // Defaults assume 5 body-mounted solar faces and a low-alpha / high-epsilon
    // zenith radiator on face 6.
    // -------------------------------------------------------------------------
    parameter Real alphaSolar[6] = {0.90, 0.90, 0.90, 0.90, 0.90, 0.20}
      "Solar absorptivity per face";
    parameter Real epsIR[6] = {0.85, 0.85, 0.85, 0.85, 0.85, 0.88}
      "IR emissivity per face";
    parameter Real earthIRAbs[6] = {0.85, 0.85, 0.85, 0.85, 0.90, 0.20}
      "Effective Earth-IR absorptance per face";
    parameter Real earthView[6] = {0.28, 0.28, 0.28, 0.28, 0.90, 0.05}
      "Approximate Earth view factor per face";
    parameter Real spaceView[6] = {0.72, 0.72, 0.72, 0.72, 0.10, 0.95}
      "Approximate deep-space view factor per face";

    // -------------------------------------------------------------------------
    // Solar panels
    // Set panelArea[i] = 0 on any face without solar cells.
    // -------------------------------------------------------------------------
    parameter Real panelArea[6] = {0.012, 0.012, 0.012, 0.012, 0.0075, 0.0}
      "Active solar-cell area per face [m2]";
    parameter Real panelEff[6] = {0.28, 0.28, 0.28, 0.28, 0.28, 0.0}
      "Reference electrical efficiency at 25 C";
    parameter Real panelTempCoeff = -0.0035
      "Relative panel efficiency slope [1/K]";
    parameter Real etaEPS = 0.80 "Net EPS efficiency after MPPT/DC-DC/cabling";

    // -------------------------------------------------------------------------
    // Lumped heat capacities
    // -------------------------------------------------------------------------
    parameter Real C_face[6] = {180, 180, 180, 180, 130, 130}
      "Effective heat capacity of each outer face [J/K]";
    parameter Real C_frame = 450 "Frame heat capacity [J/K]";
    parameter Real C_batt = 220 "Battery heat capacity [J/K]";
    parameter Real C_cm5 = 60 "CM5 + carrier effective heat capacity [J/K]";
    parameter Real T0_face[6] = fill(293.15, 6) "Initial face temperatures [K]";
    parameter Real T0_frame = 293.15 "Initial frame temperature [K]";
    parameter Real T0_batt = 293.15 "Initial battery temperature [K]";
    parameter Real T0_cm5 = 293.15 "Initial CM5 temperature [K]";

    // -------------------------------------------------------------------------
    // Conductive network
    // Increase G_cm5_face[6] and G_frame_face[6] to model a stronger strap toward
    // the zenith radiator face.
    // -------------------------------------------------------------------------
    parameter Real G_frame_face[6] = {0.45, 0.45, 0.45, 0.45, 0.35, 0.75}
      "Conductance frame -> face [W/K]";
    parameter Real G_batt_frame = 0.08 "Battery-to-frame conductance [W/K]";
    parameter Real G_cm5_frame = 0.70 "CM5-to-frame conductance [W/K]";
    parameter Real G_batt_face[6] = {0, 0, 0, 0, 0.03, 0}
      "Optional direct battery-to-face coupling [W/K]";
    parameter Real G_cm5_face[6] = {0, 0, 0, 0, 0, 0.25}
      "Optional direct CM5-to-face strap [W/K]";

    // -------------------------------------------------------------------------
    // Internal dissipations
    // Baseline follows BOREALIS-1 logic: CM5 OFF in eclipse.
    // -------------------------------------------------------------------------
    parameter Real P_battInternal = 0.0 "Battery internal dissipation [W]";
    parameter Real P_cm5_idle = 2.2 "CM5 idle / light workload dissipation [W]";
    parameter Real P_cm5_active = 4.5 "CM5 active workload dissipation [W]";
    parameter Boolean pulseCM5 = true
      "true = CM5 duty-cycled in sunlit arcs, false = always active in sunlit arcs";
    parameter Real cm5Duty = 0.20 "Fraction of each cm5Cycle at active power";
    parameter Real cm5Cycle = 600 "CM5 workload cycle [s]";

    // -------------------------------------------------------------------------
    // States
    // -------------------------------------------------------------------------
    Real T_face[6](start=T0_face) "Face temperatures [K]";
    Real T_frame(start=T0_frame) "Frame temperature [K]";
    Real T_batt(start=T0_batt) "Battery temperature [K]";
    Real T_cm5(start=T0_cm5) "CM5 temperature [K]";

    // Convenience outputs in Celsius
    Real T_face_C[6] "Face temperatures [degC]";
    Real T_frame_C "Frame temperature [degC]";
    Real T_batt_C "Battery temperature [degC]";
    Real T_cm5_C "CM5 temperature [degC]";

    // Orbital / lighting variables
    Real phi "Orbital phase [rad]";
    Real orbitAngle_deg "Orbital phase modulo 360 deg";
    Real sunVec[3] "Sun direction in LVLH/body frame";
    Real dotER "Dot(Earth->sat, sat->Sun)";
    Real earthLineDistance "Distance from Earth center to sun line [m]";
    Boolean eclipse "True when inside simplified cylindrical Earth shadow";
    Real eclipseFlag "1 in eclipse, 0 in sunlight";
    Real sunVisible "1 in sunlight, 0 in eclipse";

    // Solar / thermal outputs
    Real sunInc[6] "Direct-solar cosine incidence per face";
    Real panelPowerFace[6] "Electrical power generated by each face [W]";
    Real Q_sun[6] "Absorbed direct-solar heat [W]";
    Real Q_albedo[6] "Absorbed albedo heat [W]";
    Real Q_earthIR[6] "Absorbed Earth IR heat [W]";
    Real Q_radToSpace[6] "Radiated heat to deep space [W]";
    Real Q_frameToFace[6] "Conducted heat from frame to face [W]";
    Real Q_cm5ToFace[6] "Conducted heat from CM5 to face [W]";
    Real Q_battToFace[6] "Conducted heat from battery to face [W]";
    Real Q_faceNet[6] "Net heat rate into each face [W]";
    Real Q_externalTotal "Total external heat load on all faces [W]";

    // Power bookkeeping
    Real cm5On "0/1 indicator";
    Real P_cm5 "Instantaneous CM5 dissipation [W]";
    Real P_panelGross "Total generated panel power [W]";
    Real P_panelNet "Net solar electrical power after etaEPS [W]";
    Real E_panelGross_Wh(start=0) "Integrated gross solar energy [Wh]";
    Real E_panelNet_Wh(start=0) "Integrated net solar energy [Wh]";
    Real E_cm5_Wh(start=0) "Integrated CM5 energy use [Wh]";
  equation
    // Orbit angle
    phi = phi0 + n*time;
    orbitAngle_deg = 180.0/pi*mod(phi, 2*pi);

    // Simplified Sun vector in LVLH / body frame for nadir pointing
    sunVec[1] = cos(beta)*sin(phi);
    sunVec[2] = sin(beta);
    sunVec[3] = -cos(beta)*cos(phi);

    // Cylindrical eclipse approximation
    dotER = -sunVec[3];
    earthLineDistance = a*sqrt(max(0.0, 1.0 - dotER*dotER));
    eclipse = (dotER < 0.0) and (earthLineDistance < RE);
    eclipseFlag = if eclipse then 1.0 else 0.0;
    sunVisible = if eclipse then 0.0 else 1.0;

    // CM5 workload logic (baseline: OFF in eclipse)
    cm5On = if eclipse then 0.0 else if pulseCM5 then (if mod(time, cm5Cycle) < cm5Duty*cm5Cycle then 1.0 else 0.0) else 1.0;
    P_cm5 = if eclipse then 0.0 else (if cm5On > 0.5 then P_cm5_active else P_cm5_idle);

    for i in 1:6 loop
      sunInc[i] = sunVisible*posPart(
        faceNormal[i,1]*sunVec[1] +
        faceNormal[i,2]*sunVec[2] +
        faceNormal[i,3]*sunVec[3]);

      Q_sun[i] = solarFlux*alphaSolar[i]*A_face[i]*sunInc[i];
      Q_albedo[i] = if eclipse then 0.0 else albedo*solarFlux*alphaSolar[i]*A_face[i]*earthView[i];
      Q_earthIR[i] = earthIRFlux*earthIRAbs[i]*A_face[i]*earthView[i];
      Q_radToSpace[i] = sigma*epsIR[i]*A_face[i]*spaceView[i]*(T_face[i]^4 - Tspace^4);

      Q_frameToFace[i] = G_frame_face[i]*(T_frame - T_face[i]);
      Q_cm5ToFace[i] = G_cm5_face[i]*(T_cm5 - T_face[i]);
      Q_battToFace[i] = G_batt_face[i]*(T_batt - T_face[i]);

      Q_faceNet[i] = Q_sun[i] + Q_albedo[i] + Q_earthIR[i]
                   + Q_frameToFace[i] + Q_cm5ToFace[i] + Q_battToFace[i]
                   - Q_radToSpace[i];

      C_face[i]*der(T_face[i]) = Q_faceNet[i];

      panelPowerFace[i] = solarFlux*panelArea[i]*sunInc[i]
                        * max(0.0, panelEff[i]*(1.0 + panelTempCoeff*(T_face[i] - 298.15)));

      T_face_C[i] = T_face[i] - 273.15;
    end for;

    // Internal nodes
    C_frame*der(T_frame) = -sum(Q_frameToFace)
                         + G_cm5_frame*(T_cm5 - T_frame)
                         + G_batt_frame*(T_batt - T_frame);

    C_cm5*der(T_cm5) = P_cm5
                     - G_cm5_frame*(T_cm5 - T_frame)
                     - sum(Q_cm5ToFace);

    C_batt*der(T_batt) = P_battInternal
                       - G_batt_frame*(T_batt - T_frame)
                       - sum(Q_battToFace);

    // Power bookkeeping
    P_panelGross = sum(panelPowerFace);
    P_panelNet = etaEPS*P_panelGross;
    Q_externalTotal = sum(Q_sun) + sum(Q_albedo) + sum(Q_earthIR);

    der(E_panelGross_Wh) = P_panelGross/3600.0;
    der(E_panelNet_Wh) = P_panelNet/3600.0;
    der(E_cm5_Wh) = P_cm5/3600.0;

    // Celsius convenience outputs
    T_frame_C = T_frame - 273.15;
    T_batt_C = T_batt - 273.15;
    T_cm5_C = T_cm5 - 273.15;

    annotation(
      experiment(StartTime=0, StopTime=18000, Interval=10, Tolerance=1e-6),
      Documentation(info="<html>
<p><b>BorealisThermalConcept.LEO500kmNadir_1p5U</b></p>
<p>Conceptual lumped-parameter model for early thermal/solar trades of a 1.5U nadir-pointing CubeSat.</p>
<p><b>What it includes</b></p>
<ul>
<li>Direct solar input with eclipse logic.</li>
<li>Earth IR and a simple albedo term.</li>
<li>Six external faces + frame + battery + CM5 thermal nodes.</li>
<li>Conduction from internal nodes to frame and optional direct straps to selected faces.</li>
<li>Radiation from each outer face to deep space.</li>
<li>Solar-panel incidence and electrical generation per face.</li>
</ul>
<p><b>What it does not include</b></p>
<ul>
<li>Detailed seasonal beta history from a true SSO propagator.</li>
<li>Exact view factors, self-shadowing, antenna shadowing, or deployables.</li>
<li>Detailed internal PCB spreading, contact resistances, or MLI.</li>
<li>Battery electrochemistry, panel IV curves, or ADCS slews.</li>
</ul>
<p>Use this model for architecture trades, not for flight qualification.</p>
</html>"));
  end LEO500kmNadir_1p5U;

  model Example_CM5_To_ZenithRadiator
    "Example with stronger CM5 strap to zenith radiator face"
    extends LEO500kmNadir_1p5U(
      G_cm5_frame=0.55,
      G_cm5_face={0,0,0,0,0,0.60},
      G_frame_face={0.40,0.40,0.40,0.40,0.30,1.00});
  end Example_CM5_To_ZenithRadiator;

  model Example_Battery_MoreIsolated
    "Example with weaker battery coupling for thermal isolation"
    extends LEO500kmNadir_1p5U(
      G_batt_frame=0.04,
      G_batt_face={0,0,0,0,0.01,0});
  end Example_Battery_MoreIsolated;

  model Example_Battery_WarmingBias
    "Example with stronger passive battery warming from the structure"
    extends LEO500kmNadir_1p5U(
      G_batt_frame=0.14,
      G_batt_face={0,0,0,0,0.06,0});
  end Example_Battery_WarmingBias;

end BorealisThermalConcept;
