window.dashboard = {
  init: async function (dotnetRef) {
    this.dotnetRef = dotnetRef;
    this.terminal = document.getElementById('terminal');
    this.hud = document.getElementById('attitudeHud');
    this.maxLines = 160;
    this.lines = [];
    this.pendingRaw = [];
    this.lastTerminalFlush = 0;
    this.lastChartUpdate = 0;
    this.last3dUpdate = 0;
    this.mode = 'all';
    this.follow = true;
    this.showAxisDebug = false;
    this.referenceQuat = null;
    this.currentQuat = null;
    this.modelAlignmentQuat = null;

    this.initCube();
    this.initChart();
    this.signalWindowSec = 10;
    this.signalTrendRangeSec = 600;
    this.signalTrendZoomSec = 600;
    this.signalQualityHistory = [];
    this.initSignalQualityChart();
    this.initSignalQualityTrendChart();

    if (!window.signalR) {
      this.pushRaw('#WARN signalR no está disponible en el cliente.');
      return;
    }

    const conn = new signalR.HubConnectionBuilder().withUrl('/hubs/telemetry').build();
    conn.on('rawLine', (line) => this.enqueueRaw(line));
    conn.on('telemetrySample', (sample) => this.pushSample(sample));
    conn.on('telemetryStats', (stats) => this.pushStats(stats));
    await conn.start();
  },

  setDotNetRef: function (dotnetRef) { this.dotnetRef = dotnetRef; },
  setTheme: function(theme){ document.documentElement.setAttribute('data-theme', theme); },
  setFollow: function(follow){ this.follow = !!follow; if (this.controls) this.controls.enabled = !this.follow; },
  toggleAxisDebug: function(){ this.showAxisDebug = !this.showAxisDebug; },

  setReference: function() {
    if (!this.referenceQuat || !this.currentQuat) return;
    this.referenceQuat.copy(this.currentQuat);
    localStorage.setItem('dashboard.qref', JSON.stringify({
      x: this.referenceQuat.x, y: this.referenceQuat.y, z: this.referenceQuat.z, w: this.referenceQuat.w
    }));
    this.pushRaw('#INFO reference set');
  },

  restoreReference: function() {
    if (!window.THREE || !this.referenceQuat) return;
    try {
      const raw = localStorage.getItem('dashboard.qref');
      if (!raw) return;
      const q = JSON.parse(raw);
      if (q && Number.isFinite(q.x) && Number.isFinite(q.y) && Number.isFinite(q.z) && Number.isFinite(q.w)) {
        this.referenceQuat.copy(new THREE.Quaternion(q.x, q.y, q.z, q.w).normalize());
      }
    } catch {}
  },

  pushStats: async function (stats) {
    this.updateSignalQuality(stats);
    if (!this.dotnetRef) return;
    try { await this.dotnetRef.invokeMethodAsync('OnStats', stats); } catch {}
  },


  initSignalQualityChart: function () {
    if (!window.Chart) { return; }
    const ctx = document.getElementById('signalQualityChart');
    this.signalQualityValue = document.getElementById('signalQualityValue');
    if (!ctx) return;
    this.signalQualityChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['OK', 'Lost'],
        datasets: [{
          data: [1, 0],
          backgroundColor: ['#22c55e', '#ef4444'],
          borderWidth: 0
        }]
      },
      options: {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  },


  formatRelativeTimeLabel: function(secondsAgo) {
    const s = Math.max(0, Math.round(secondsAgo));
    if (s >= 60) {
      const m = Math.floor(s / 60);
      const rs = s % 60;
      return rs === 0 ? `T - ${m}m` : `T - ${m}m ${rs}s`;
    }
    return `T - ${s}s`;
  },

  renderSignalQualityTrend: function() {
    if (!this.signalQualityTrendChart) return;
    const now = Date.now();
    const minTs = now - (this.signalTrendZoomSec * 1000);
    const points = this.signalQualityHistory.filter(p => p.at >= minTs);
    const trend = this.signalQualityTrendChart.data;
    trend.labels = points.map(p => this.formatRelativeTimeLabel((now - p.at) / 1000));
    trend.datasets[0].data = points.map(p => p.value);
    this.signalQualityTrendChart.update('none');
  },

  initSignalQualityTrendChart: function () {
    if (!window.Chart) { return; }
    const ctx = document.getElementById('signalQualityTrendChart');
    if (!ctx) return;
    this.signalQualityTrendChart = new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets: [{
        label: 'Quality %',
        data: [],
        borderColor: '#60a5fa',
        pointRadius: 0,
        tension: 0.25
      }] },
      options: {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100 },
          x: { ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 8 } }
        }
      }
    });

    ctx.addEventListener('wheel', (ev) => {
      ev.preventDefault();
      const dir = ev.deltaY > 0 ? 1 : -1;
      const next = this.signalTrendZoomSec + (dir * 5);
      this.signalTrendZoomSec = Math.min(this.signalTrendRangeSec, Math.max(10, next));
      this.renderSignalQualityTrend();
    }, { passive: false });

    ctx.addEventListener('dblclick', () => {
      this.signalTrendZoomSec = this.signalTrendRangeSec;
      this.renderSignalQualityTrend();
    });
  },

  updateSignalQuality: function (stats) {
    if (!stats) return;
    const ok = Number(stats.okCountWindow ?? stats.OkCountWindow ?? stats.okCount ?? stats.OkCount ?? 0);
    const lost = Number(stats.lostCountWindow ?? stats.LostCountWindow ?? stats.lostCountEstimado ?? stats.LostCountEstimado ?? 0);
    const total = ok + lost;
    const success = total > 0 ? (ok / total) : 1;

    if (this.signalQualityValue) {
      this.signalQualityValue.textContent = `${(success * 100).toFixed(1)}%`;
    }

    if (this.signalQualityChart) {
      const ds = this.signalQualityChart.data.datasets[0];
      ds.data[0] = ok;
      ds.data[1] = lost;
      this.signalQualityChart.update('none');
    }

    const now = Date.now();
    this.signalQualityHistory.push({ at: now, value: success * 100 });
    const minTs = now - (this.signalTrendRangeSec * 1000);
    this.signalQualityHistory = this.signalQualityHistory.filter(p => p.at >= minTs);
    this.renderSignalQualityTrend();
  },

  initCube: function () {
    if (!window.THREE) { this.pushRaw('#WARN three.js no está disponible; vista 3D deshabilitada.'); return; }
    const mount = document.getElementById('cube');
    this.referenceQuat = new THREE.Quaternion(0, 0, 0, 1);
    this.currentQuat = new THREE.Quaternion(0, 0, 0, 1);
    this.modelAlignmentQuat = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, 0));
    this.restoreReference();
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x070b12);
    const camera = new THREE.PerspectiveCamera(70, mount.clientWidth / mount.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    mount.appendChild(renderer.domElement);

    const geo = new THREE.BoxGeometry(0.7, 1, 0.25);
    const mat = new THREE.MeshStandardMaterial({ color: 0x9ca3af, metalness: 0.4, roughness: 0.5 });
    this.cube = new THREE.Mesh(geo, mat);
    scene.add(this.cube);

    const horizon = new THREE.GridHelper(8, 20, 0x29466b, 0x1a2b45);
    horizon.position.y = -1.2;
    scene.add(horizon);
    scene.add(new THREE.AxesHelper(1.8));

    const light = new THREE.DirectionalLight(0xffffff, 0.9);
    light.position.set(3, 3, 4);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x6b7280, 0.4));

    camera.position.set(2.8, 1.6, 2.8);
    camera.lookAt(0, 0, 0);
    this.followOffset = new THREE.Vector3(2.8, 1.6, 2.8);

    this.scene = scene;
    this.camera = camera;
    this.renderer = renderer;

    if (THREE.OrbitControls) {
      this.controls = new THREE.OrbitControls(camera, renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.enabled = !this.follow;
    }

    const animate = () => {
      requestAnimationFrame(animate);
      if (this.follow && this.cube) {
        const followPos = this.followOffset.clone().applyQuaternion(this.cube.quaternion);
        camera.position.copy(followPos);
        camera.lookAt(this.cube.position);
      } else if (this.controls) {
        this.controls.update();
      }
      renderer.render(scene, camera);
    };
    animate();
  },

  initChart: function () {
    if (!window.Chart) { this.pushRaw('#WARN chart.js no está disponible; gráfico deshabilitado.'); return; }
    const ctx = document.getElementById('telemetryChart');
    this.chart = new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets: [
        { label: 'ax', data: [], borderColor: '#38bdf8' },
        { label: 'ay', data: [], borderColor: '#60a5fa' },
        { label: 'az', data: [], borderColor: '#22d3ee' },
        { label: 'gx', data: [], borderColor: '#a78bfa' },
        { label: 'gy', data: [], borderColor: '#f59e0b' },
        { label: 'gz', data: [], borderColor: '#34d399' },
        { label: 'q0', data: [], borderColor: '#f472b6' },
        { label: 'q1', data: [], borderColor: '#fb7185' },
        { label: 'q2', data: [], borderColor: '#818cf8' },
        { label: 'q3', data: [], borderColor: '#2dd4bf' }
      ]},
      options: { animation: false, responsive: true, maintainAspectRatio: false }
    });
  },

  setMode: function(mode){
    if(!this.chart) return;
    this.chart.data.datasets.forEach((ds, i) => {
      if (mode === 'all') ds.hidden = false;
      else if (mode === 'accel') ds.hidden = i > 2;
      else if (mode === 'gyro') ds.hidden = i < 3 || i > 5;
      else if (mode === 'quat') ds.hidden = i < 6;
    });
    this.chart.update('none');
  },

  enqueueRaw: function(line) {
    this.pendingRaw.push(line);
    const now = performance.now();
    if (now - this.lastTerminalFlush > 200) { this.flushRaw(); this.lastTerminalFlush = now; }
  },

  flushRaw: function() {
    if (this.pendingRaw.length === 0) return;
    for (const line of this.pendingRaw) {
      this.lines.push(line);
      if (this.lines.length > this.maxLines) this.lines.shift();
    }
    this.pendingRaw = [];
    if (!this.terminal) return;
    this.terminal.textContent = this.lines.join('\n');
    this.terminal.scrollTop = this.terminal.scrollHeight;
  },

  pushRaw: function (line) { this.enqueueRaw(line); this.flushRaw(); },



  getNum: function (obj, camel, pascal, fallback) {
    const v = obj?.[camel] ?? obj?.[pascal];
    return Number.isFinite(v) ? v : fallback;
  },

  getDateValue: function (obj, camel, pascal) {
    return obj?.[camel] ?? obj?.[pascal] ?? new Date().toISOString();
  },
  updateHud: function(q) {
    if (!this.hud) return;
    const e = new THREE.Euler().setFromQuaternion(q, 'XYZ');
    const r = THREE.MathUtils.radToDeg(e.x).toFixed(1);
    const p = THREE.MathUtils.radToDeg(e.y).toFixed(1);
    const y = THREE.MathUtils.radToDeg(e.z).toFixed(1);
    this.hud.textContent = `roll=${r} pitch=${p} yaw=${y}`;
  },

  pushSample: function (s) {
    const now = performance.now();

    if (this.cube && now - this.last3dUpdate > 50) {
      const qw = this.getNum(s, 'q0', 'Q0', 1.0);
      const qx = this.getNum(s, 'q1', 'Q1', 0.0);
      const qy = this.getNum(s, 'q2', 'Q2', 0.0);
      const qz = this.getNum(s, 'q3', 'Q3', 0.0);

      const qCurrent = new THREE.Quaternion(qx, qy, qz, qw).normalize();
      if (this.currentQuat) this.currentQuat.copy(qCurrent);

      const reference = this.referenceQuat ?? new THREE.Quaternion(0, 0, 0, 1);
      const alignment = this.modelAlignmentQuat ?? new THREE.Quaternion(0, 0, 0, 1);
      const qDisplay = reference.clone().invert().multiply(qCurrent).multiply(alignment).normalize();
      this.cube.quaternion.copy(qDisplay);
      this.updateHud(qDisplay);

      if (this.showAxisDebug) {
        const axDbg = this.getNum(s, 'ax', 'Ax', 0);
        const ayDbg = this.getNum(s, 'ay', 'Ay', 0);
        const azDbg = this.getNum(s, 'az', 'Az', 0);
        const gxDbg = this.getNum(s, 'gx', 'Gx', 0);
        const gyDbg = this.getNum(s, 'gy', 'Gy', 0);
        const gzDbg = this.getNum(s, 'gz', 'Gz', 0);
        this.pushRaw(`#AXIS,ax=${axDbg},ay=${ayDbg},az=${azDbg},gx=${gxDbg},gy=${gyDbg},gz=${gzDbg},qw=${qw.toFixed(3)},qx=${qx.toFixed(3)},qy=${qy.toFixed(3)},qz=${qz.toFixed(3)}`);
      }
      this.last3dUpdate = now;
    }

    if (!this.chart) return;

    const receivedAt = this.getDateValue(s, 'receivedAtUtc', 'ReceivedAtUtc');
    const t = new Date(receivedAt).toLocaleTimeString();
    const data = this.chart.data;
    data.labels.push(t);
    const values = [
      this.getNum(s, 'ax', 'Ax', 0),
      this.getNum(s, 'ay', 'Ay', 0),
      this.getNum(s, 'az', 'Az', 0),
      this.getNum(s, 'gx', 'Gx', 0),
      this.getNum(s, 'gy', 'Gy', 0),
      this.getNum(s, 'gz', 'Gz', 0),
      this.getNum(s, 'q0', 'Q0', 1),
      this.getNum(s, 'q1', 'Q1', 0),
      this.getNum(s, 'q2', 'Q2', 0),
      this.getNum(s, 'q3', 'Q3', 0)
    ];
    data.datasets.forEach((ds, i) => ds.data.push(values[i]));

    if (data.labels.length > 180) {
      data.labels.shift();
      data.datasets.forEach(ds => ds.data.shift());
    }

    if (now - this.lastChartUpdate > 100) {
      this.chart.update('none');
      this.lastChartUpdate = now;
    }
  }
};
