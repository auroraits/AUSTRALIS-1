# Consolida documentaci�n/texto y c�digo fuente en 2 archivos:
#  - CONSOLIDADO.md
#  - CODIGO_FUENTE.txt
# Robusto contra locks: escribe en .tmp y luego reemplaza (rename/overwrite).
# Evita archivos > 1MB. Excluye carpetas indeseables. Heur�stica de texto plano.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $root) { $root = (Get-Location).Path }

$docsOut = Join-Path $root "CONSOLIDADO.md"
$codeOut = Join-Path $root "CODIGO_FUENTE.txt"

$docsTmp = $docsOut + ".tmp"
$codeTmp = $codeOut + ".tmp"

$MaxBytes = 1MB

$ExcludedDirNames = @(
  ".git",".svn",".hg",
  ".vs",".vscode",".idea",
  "bin","obj","Debug","Release","x64","x86","AnyCPU",".artifacts","artifacts",
  "TestResults","packages",
  "node_modules","bower_components","dist","build","out","coverage",".next",".nuxt",
  "__pycache__", ".pytest_cache", ".mypy_cache",
  ".gradle",".m2",".ivy2",
  ".terraform",".serverless",".cache",".tmp","tmp",
  "target","venv",
  # Arduino/PlatformIO/ESP-IDF builds (excluir outputs, incluir sketch/src/lib)
  ".pio",".platformio",".arduinoIDE","build-arduino","cmake-build-debug","cmake-build-release",
  "CMakeFiles",".espressif","managed_components","granite_model", "granite_cubesat_lora"
)

$CodeExt = @(
  ".cs",".csx",".csproj",".sln",".props",".targets",".nuspec",
  ".vb",".fs",
  ".cpp",".c",".h",".hpp",".hh",".ino",".pde",".cxx",".cc",
  ".py",".java",".kt",".go",".rs",".swift",".m",".mm",
  ".js",".ts",".jsx",".tsx",".json",
  ".html",".htm",".css",".scss",".less",
  ".sql",
  ".ps1",".psm1",".psd1",".sh",".bash",".zsh",".bat",".cmd",
  ".yml",".yaml",".xml",".ini",".cfg",".conf",".config",".toml",".env",
  ".proto",".graphql",".gql",
  ".make",".mk"
)

$DocsExt = @(
  ".md",".txt",".log",".rst",".adoc",".org",
  ".csv",".tsv"
)

function Test-IsProbablyBinary {
  param([Parameter(Mandatory)][string]$Path)
  try {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $len = [Math]::Min($bytes.Length, 4096)
    for ($i = 0; $i -lt $len; $i++) {
      if ($bytes[$i] -eq 0) { return $true }
    }
    return $false
  } catch {
    return $false
  }
}

function Test-IsInExcludedDir {
  param([Parameter(Mandatory)][string]$FullPath)
  $parts = $FullPath.Split([System.IO.Path]::DirectorySeparatorChar, [System.StringSplitOptions]::RemoveEmptyEntries)
  foreach ($p in $parts) {
    if ($ExcludedDirNames -contains $p) { return $true }
  }
  return $false
}

function Get-FileBucket {
  param([Parameter(Mandatory)][System.IO.FileInfo]$File)

  $extLower = $File.Extension.ToLowerInvariant()

  if ($File.Name -eq "Makefile" -or $File.Name.ToLowerInvariant().EndsWith(".mk")) { return "code" }
  if ($CodeExt -contains $extLower) { return "code" }
  if ($DocsExt -contains $extLower) { return "docs" }

  if (-not (Test-IsProbablyBinary -Path $File.FullName)) { return "docs" }
  return "skip"
}

# Escribe un texto a un archivo con retry por locks (por si el tmp tambi�n lo engancha algo)
function Write-AllTextWithRetry {
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][string]$Content,
    [int]$Retries = 20,
    [int]$DelayMs = 250
  )

  for ($i = 1; $i -le $Retries; $i++) {
    try {
      # Abrimos el archivo con "share read" para no pelear con lectores
      $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
      $fs = New-Object System.IO.FileStream($Path, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
      try {
        $sw = New-Object System.IO.StreamWriter($fs, $utf8NoBom)
        try { $sw.Write($Content) } finally { $sw.Dispose() }
      } finally { $fs.Dispose() }

      return
    } catch {
      if ($i -eq $Retries) { throw }
      Start-Sleep -Milliseconds $DelayMs
    }
  }
}

# Reemplaza destino por tmp, con retry (lock t�pico por editor/preview)
function Replace-FileWithRetry {
  param(
    [Parameter(Mandatory)][string]$Tmp,
    [Parameter(Mandatory)][string]$Dest,
    [int]$Retries = 20,
    [int]$DelayMs = 250
  )

  for ($i = 1; $i -le $Retries; $i++) {
    try {
      Move-Item -LiteralPath $Tmp -Destination $Dest -Force
      return
    } catch {
      if ($i -eq $Retries) { throw }
      Start-Sleep -Milliseconds $DelayMs
    }
  }
}

$sep1 = ("=" * 110)
$sep2 = ("-" * 110)

$docsSb = New-Object System.Text.StringBuilder
$codeSb = New-Object System.Text.StringBuilder

# === BANNER DE ADVERTENCIA DE PRECEDENCIA DOCUMENTAL ===
$banner = @"
$sep1
⚠  AVISO CRÍTICO — PRECEDENCIA DOCUMENTAL OBLIGATORIA
$sep1
Este bundle (CONSOLIDADO.md) concatena documentos ACTIVOS e HISTÓRICOS del repositorio DIY Nanosat.
Mezcla material normativo, preliminar, superseded y de historial. Leer con la siguiente jerarquía:

PRECEDENCIA ESTRICTA (ante contradicción, prevalece el nivel más alto):
  1. ADR Accepted  (08_Decisions/ADR-*.md, estado: Accepted)         ← máxima autoridad
  2. 00_MVP/MVP v2.2.md                                               ← baseline consolidado vigente
  3. SYSTEM_BASELINE.md                                               ← resumen de baseline
  4. Documentación activa por subsistema (Estado: Active/Baseline)
  5. Documentos Draft / Proposed / Preliminary                        ← contexto técnico; NO normativo
  6. Histórico / Superseded / Historical Snapshot                     ← solo trazabilidad

REGLAS DE USO DE ESTE BUNDLE:
  - Un documento Draft, Proposed o Preliminary NO sobreescribe un ADR Accepted ni el baseline.
  - Los snapshots históricos y versiones viejas del MVP (v1, v2.0, v2.1) NO son fuente normativa.
  - "SCIENCE MODE" como tercer modo operativo es nomenclatura SUPERSEDADA. Usar MISSION_MODE=NOMINAL.
  - HV/Geiger fue REMOVIDO del MVP (ADR-20260218-geiger-removed-from-mvp.md). No reactivar.
  - BW definitivo del uplink LoRa sigue TBD. BW250 es candidato preferente; BW125 requiere evidencia.
  - CONF-01 (pico EPS) sigue abierto. No resolver sin medición de hardware TX real.
  - Hardware RF orbital (PCB TTC UHF + LoRa RX) NO existe todavía. Documentación es diseño objetivo.
  - OpenLST es candidato técnico/análisis. NO es baseline TTC final. RFFM6403 es EOL.

Ver AGENTS.md y architecture.md para la política completa de precedencia y gobierno documental.
Generado automáticamente por consolidar.ps1. Fecha de generación no está grabada aquí; revisar git log.
$sep1

"@
[void]$docsSb.AppendLine($banner)

$files = Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue |
  Where-Object {
    $_.FullName -ne $docsOut -and $_.FullName -ne $codeOut -and $_.FullName -ne $docsTmp -and $_.FullName -ne $codeTmp
  } |
  Where-Object { -not (Test-IsInExcludedDir -FullPath $_.FullName) } |
  Where-Object { $_.Length -le $MaxBytes } |
  Sort-Object FullName

foreach ($f in $files) {
  $bucket = Get-FileBucket -File $f
  if ($bucket -eq "skip") { continue }

  $sb = if ($bucket -eq "code") { $codeSb } else { $docsSb }

  [void]$sb.AppendLine($sep1)
  [void]$sb.AppendLine("FILE: " + $f.FullName)
  [void]$sb.AppendLine($sep2)

  try {
    $content = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop
    [void]$sb.AppendLine($content)
  } catch {
    [void]$sb.AppendLine("[WARN] No se pudo leer como texto: " + $_.Exception.Message)
  }

  [void]$sb.AppendLine()
}

# Volcado a temporales
Write-AllTextWithRetry -Path $docsTmp -Content $docsSb.ToString()
Write-AllTextWithRetry -Path $codeTmp -Content $codeSb.ToString()

# Reemplazo final (con retry)
Replace-FileWithRetry -Tmp $docsTmp -Dest $docsOut
Replace-FileWithRetry -Tmp $codeTmp -Dest $codeOut

Write-Host "OK -> Docs/Texto: $docsOut"
Write-Host "OK -> C�digo:     $codeOut"
