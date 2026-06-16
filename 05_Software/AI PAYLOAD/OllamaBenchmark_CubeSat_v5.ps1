param(
  [Parameter(Mandatory=$true, Position=0)]
  [string[]]$Models,

  [string]$SuiteFile = (Join-Path $PSScriptRoot 'CubeSatBenchmarkSuite.json'),

  [string]$OutDir = (Join-Path (Get-Location) ("ollama_cubesat_benchmark_" + (Get-Date -Format "yyyyMMdd_HHmmss"))),

  [int]$Repeats = 2,
  [int]$WarmupDelaySec = 1,
  [int]$KeepAliveSeconds = 600,
  [int]$NumPredict = 300,
  [double]$Temperature = 0,
  [int]$Seed = 42,
  [switch]$NoWarmup
)

$ErrorActionPreference = "Stop"
$endpoint = "http://127.0.0.1:11434/api/chat"
$versionEndpoint = "http://127.0.0.1:11434/api/version"

function Sanitize-FileName {
  param([string]$Name)
  $invalid = [IO.Path]::GetInvalidFileNameChars()
  foreach ($ch in $invalid) { $Name = $Name.Replace($ch, "_") }
  $Name = $Name.Replace(":", "_").Replace("/", "_").Replace("\", "_")
  return $Name
}

function New-JsonBody {
  param(
    [string]$Model,
    [string]$SystemPrompt,
    [string]$UserPrompt,
    [hashtable]$Options,
    [int]$KeepAliveSeconds
  )

  $messages = @()
  if ($SystemPrompt) {
    $messages += @{ role = 'system'; content = $SystemPrompt }
  }
  $messages += @{ role = 'user'; content = $UserPrompt }

  $body = [ordered]@{
    model = $Model
    stream = $false
    keep_alive = $KeepAliveSeconds
    messages = $messages
    options = $Options
  }

  return ($body | ConvertTo-Json -Depth 8 -Compress)
}

function Invoke-OllamaChat {
  param(
    [Parameter(Mandatory=$true)][string]$Model,
    [Parameter(Mandatory=$true)][string]$SystemPrompt,
    [Parameter(Mandatory=$true)][string]$UserPrompt,
    [Parameter(Mandatory=$true)][int]$KeepAliveSeconds,
    [Parameter(Mandatory=$true)][hashtable]$Options
  )

  $bodyJson = New-JsonBody -Model $Model -SystemPrompt $SystemPrompt -UserPrompt $UserPrompt -Options $Options -KeepAliveSeconds $KeepAliveSeconds
  $tmp = Join-Path $env:TEMP ("ollama_req_" + [Guid]::NewGuid().ToString("N") + ".json")
  [System.IO.File]::WriteAllText($tmp, $bodyJson, [System.Text.UTF8Encoding]::new($false))

  $resp = & curl.exe -s -H "Content-Type: application/json" --data-binary "@$tmp" $endpoint
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue

  if (-not $resp) { throw "Ollama devolvió respuesta vacía." }
  $r = $resp | ConvertFrom-Json
  if ($r.error) { throw $r.error }

  $content = $null
  $thinking = $null
  $toolCalls = $null
  if ($r.message) {
    if ($null -ne $r.message.content) { $content = [string]$r.message.content }
    if ($r.message.thinking) { $thinking = [string]$r.message.thinking }
    if ($r.message.tool_calls) { $toolCalls = $r.message.tool_calls }
  } elseif ($r.response) {
    if ($null -ne $r.response) { $content = [string]$r.response }
    if ($r.thinking) { $thinking = [string]$r.thinking }
  }

  $pt = 0
  if ($r.prompt_eval_duration -gt 0) { $pt = $r.prompt_eval_count / ($r.prompt_eval_duration/1e9) }

  $gt = 0
  if ($r.eval_duration -gt 0) { $gt = $r.eval_count / ($r.eval_duration/1e9) }

  [pscustomobject]@{
    model         = $Model
    prompt_tok_s  = [math]::Round($pt, 2)
    gen_tok_s     = [math]::Round($gt, 2)
    load_s        = [math]::Round(($r.load_duration/1e9), 3)
    total_s       = [math]::Round(($r.total_duration/1e9), 3)
    prompt_tokens = $r.prompt_eval_count
    gen_tokens    = $r.eval_count
    response      = $content
    thinking      = $thinking
    tool_calls    = $toolCalls
    done_reason   = $r.done_reason
    raw_json      = $resp
  }
}

function Save-TextFile {
  param([string]$Path,[string]$Text)
  [System.IO.File]::WriteAllText($Path, $Text, [System.Text.UTF8Encoding]::new($false))
}

function ConvertTo-JsonSafe {
  param([object]$Obj)
  try {
    return ($Obj | ConvertTo-Json -Depth 12)
  } catch {
    return "{}"
  }
}

function Test-ArrayPrefix {
  param($Actual, $Expected)
  if ($null -eq $Actual) { return $false }
  if (-not ($Actual -is [System.Collections.IEnumerable])) { return $false }
  $act = @($Actual)
  $exp = @($Expected)
  if ($act.Count -lt $exp.Count) { return $false }
  for ($i = 0; $i -lt $exp.Count; $i++) {
    if ([string]$act[$i] -ne [string]$exp[$i]) { return $false }
  }
  return $true
}

function Test-ArrayEquals {
  param($Actual, $Expected)
  $act = @($Actual)
  $exp = @($Expected)
  if ($act.Count -ne $exp.Count) { return $false }
  for ($i = 0; $i -lt $exp.Count; $i++) {
    if ([string]$act[$i] -ne [string]$exp[$i]) { return $false }
  }
  return $true
}

function Test-ArrayContainsAll {
  param($Actual, $Expected)
  $act = @($Actual) | ForEach-Object { [string]$_ }
  foreach ($e in @($Expected)) {
    if (-not ($act -contains [string]$e)) { return $false }
  }
  return $true
}


function Normalize-JsonCandidate {
  param([AllowEmptyString()][string]$Text)
  if ($null -eq $Text) { return "" }
  $t = [string]$Text
  $m = [regex]::Match($t, '(?s)```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```')
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  $startObj = $t.IndexOf('{')
  $endObj = $t.LastIndexOf('}')
  if ($startObj -ge 0 -and $endObj -gt $startObj) {
    return $t.Substring($startObj, $endObj - $startObj + 1).Trim()
  }
  $startArr = $t.IndexOf('[')
  $endArr = $t.LastIndexOf(']')
  if ($startArr -ge 0 -and $endArr -gt $startArr) {
    return $t.Substring($startArr, $endArr - $startArr + 1).Trim()
  }
  return $t.Trim()
}

function Evaluate-Response {
  param(
    [Parameter(Mandatory=$true)]$TestCase,
    [Parameter(Mandatory=$false)][AllowEmptyString()][string]$RawResponse,
    [Parameter(Mandatory=$false)]$ToolCalls
  )

  $jsonValid = $false
  $parsed = $null
  $normalized = Normalize-JsonCandidate -Text $RawResponse
  try {
    $parsed = $normalized | ConvertFrom-Json
    if ($null -ne $parsed) {
      $jsonValid = $true
    } else {
      $jsonValid = $false
    }
  } catch {
    $jsonValid = $false
  }

  $requiredKeysOk = $true
  $expectedEqualsOk = $true
  $arrayPrefixOk = $true
  $arrayEqualsOk = $true
  $arrayContainsOk = $true
  $forbiddenOk = $true

  if ($jsonValid) {
    foreach ($k in @($TestCase.requiredKeys)) {
      $propNames = @($parsed.PSObject.Properties | ForEach-Object { $_.Name })
        if (-not ($propNames -contains [string]$k)) {
        $requiredKeysOk = $false
      }
    }

    if ($TestCase.expectedEquals) {
      foreach ($p in $TestCase.expectedEquals.PSObject.Properties) {
        if ([string]$parsed.$($p.Name) -ne [string]$p.Value) {
          $expectedEqualsOk = $false
        }
      }
    }

    if ($TestCase.arrayPrefixEquals) {
      foreach ($p in $TestCase.arrayPrefixEquals.PSObject.Properties) {
        if (-not (Test-ArrayPrefix -Actual $parsed.$($p.Name) -Expected $p.Value)) {
          $arrayPrefixOk = $false
        }
      }
    }

    if ($TestCase.arrayEquals) {
      foreach ($p in $TestCase.arrayEquals.PSObject.Properties) {
        if (-not (Test-ArrayEquals -Actual $parsed.$($p.Name) -Expected $p.Value)) {
          $arrayEqualsOk = $false
        }
      }
    }

    if ($TestCase.arrayContains) {
      foreach ($p in $TestCase.arrayContains.PSObject.Properties) {
        if (-not (Test-ArrayContainsAll -Actual $parsed.$($p.Name) -Expected $p.Value)) {
          $arrayContainsOk = $false
        }
      }
    }
  } else {
    $requiredKeysOk = $false
    $expectedEqualsOk = $false
    $arrayPrefixOk = $false
    $arrayEqualsOk = $false
    $arrayContainsOk = $false
  }

  foreach ($f in @($TestCase.forbiddenSubstrings)) {
    if (($null -ne $RawResponse) -and ($RawResponse -match [regex]::Escape([string]$f))) {
      $forbiddenOk = $false
    }
  }

  $checks = @(
    $jsonValid,
    $requiredKeysOk,
    $expectedEqualsOk,
    $arrayPrefixOk,
    $arrayEqualsOk,
    $arrayContainsOk,
    $forbiddenOk
  )
  $score = ($checks | Where-Object { $_ }).Count

  [pscustomobject]@{
    json_valid = $jsonValid
    required_keys_ok = $requiredKeysOk
    expected_equals_ok = $expectedEqualsOk
    array_prefix_ok = $arrayPrefixOk
    array_equals_ok = $arrayEqualsOk
    array_contains_ok = $arrayContainsOk
    forbidden_ok = $forbiddenOk
    score = $score
    max_score = $checks.Count
    pass = ($score -eq $checks.Count)
    parsed = $parsed
    tool_calls = $ToolCalls
    normalized = $normalized
  }
}

function ToMarkdownTable {
  param(
    [Parameter(Mandatory=$true)][object[]]$Rows,
    [Parameter(Mandatory=$true)][string[]]$Columns,
    [Parameter(Mandatory=$true)][hashtable]$Headers
  )

  $hdrCells = @()
  foreach ($c in $Columns) {
    $name = if ($Headers.ContainsKey($c)) { $Headers[$c] } else { $c }
    $hdrCells += (" " + $name + " ")
  }
  $hdr = "|" + ($hdrCells -join "|") + "|"
  $sep = "|" + (($Columns | ForEach-Object { " --- " }) -join "|") + "|"

  $lines = New-Object System.Collections.Generic.List[string]
  $lines.Add($hdr)
  $lines.Add($sep)

  foreach ($r in $Rows) {
    $cells = @()
    foreach ($c in $Columns) {
      $v = $r.$c
      if ($null -eq $v) { $cells += " " } else { $cells += (" " + $v.ToString() + " ") }
    }
    $lines.Add("|" + ($cells -join "|") + "|")
  }
  return ($lines -join "`n")
}

if ($Models.Count -eq 1 -and $Models[0].Contains(",")) {
  $Models = $Models[0].Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
}

try {
  $null = Invoke-RestMethod -Uri $versionEndpoint -Method Get
} catch {
  throw "No puedo conectar a Ollama en http://127.0.0.1:11434. Asegurate de que Ollama esté corriendo."
}

if (-not (Test-Path $SuiteFile)) {
  throw "No encuentro el suite file: $SuiteFile"
}

$suite = Get-Content -Raw -Path $SuiteFile | ConvertFrom-Json
$systemPrompt = [string]$suite.systemPrompt
$tests = @($suite.tests)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$ResponsesDir = Join-Path $OutDir "responses"
New-Item -ItemType Directory -Force -Path $ResponsesDir | Out-Null

$options = @{
  temperature = $Temperature
  seed = $Seed
  num_predict = $NumPredict
}

$results = @()
Write-Host ("Models: " + ($Models -join ", ")) -ForegroundColor Cyan
Write-Host ("Suite: " + $SuiteFile) -ForegroundColor DarkGray
Write-Host ("OutDir: " + $OutDir) -ForegroundColor DarkGray

foreach ($m in $Models) {
  Write-Host ""
  Write-Host ("=== " + $m + " ===") -ForegroundColor Yellow

  if (-not $NoWarmup) {
    try {
      $warmPrompt = 'Responde solo con {"case_id":"WARMUP","recommended_action":"NOOP","ai_payload_state":"UNCHANGED","mission_mode":"UNCHANGED","downlink_priority":[],"selected_items":[],"confidence":0.0,"rationale":[],"constraints_checked":[],"notes":"warmup"}'
      $warm = Invoke-OllamaChat -Model $m -SystemPrompt $systemPrompt -UserPrompt $warmPrompt -KeepAliveSeconds $KeepAliveSeconds -Options $options
      Start-Sleep -Seconds $WarmupDelaySec
    } catch {
      Write-Warning ("Warmup falló para ${m}: " + $_.Exception.Message)
    }
  }

  foreach ($t in $tests) {
    for ($r = 1; $r -le $Repeats; $r++) {
      $effectiveSystem = $systemPrompt
      if ($t.policyPrompt) {
        $effectiveSystem = $effectiveSystem + "`n`n" + [string]$t.policyPrompt
      }

      $run = Invoke-OllamaChat -Model $m -SystemPrompt $effectiveSystem -UserPrompt ([string]$t.userPrompt) -KeepAliveSeconds $KeepAliveSeconds -Options $options
      $eval = Evaluate-Response -TestCase $t -RawResponse ([string]$run.response) -ToolCalls $run.tool_calls

      $safeModel = Sanitize-FileName -Name $m
      $safeCase = Sanitize-FileName -Name ([string]$t.id)
      $base = "{0}_{1}_run{2}" -f $safeModel, $safeCase, $r

      Save-TextFile -Path (Join-Path $ResponsesDir ($base + ".prompt.txt")) -Text ([string]$t.userPrompt)
      Save-TextFile -Path (Join-Path $ResponsesDir ($base + ".response.json")) -Text ([string]$run.response)
      Save-TextFile -Path (Join-Path $ResponsesDir ($base + ".thinking.txt")) -Text ([string]$run.thinking)
      Save-TextFile -Path (Join-Path $ResponsesDir ($base + ".eval.json")) -Text (ConvertTo-JsonSafe $eval)

      $row = [pscustomobject]@{
        model = $m
        test_id = [string]$t.id
        category = [string]$t.category
        run = $r
        json_valid = $eval.json_valid
        pass = $eval.pass
        score = "$($eval.score)/$($eval.max_score)"
        prompt_tok_s = $run.prompt_tok_s
        gen_tok_s = $run.gen_tok_s
        load_s = $run.load_s
        total_s = $run.total_s
        prompt_tokens = $run.prompt_tokens
        gen_tokens = $run.gen_tokens
      }
      $results += $row
      Write-Host ("{0} run{1}: pass={2} score={3} gen_tok_s={4} total_s={5}" -f $t.id, $r, $eval.pass, $row.score, $row.gen_tok_s, $row.total_s)
      Start-Sleep -Milliseconds 250
    }
  }

  try {
    $unloadPrompt = '{"case_id":"UNLOAD","recommended_action":"NOOP","ai_payload_state":"UNCHANGED","mission_mode":"UNCHANGED","downlink_priority":[],"selected_items":[],"confidence":0.0,"rationale":[],"constraints_checked":[],"notes":"unload"}'
    $null = Invoke-OllamaChat -Model $m -SystemPrompt $systemPrompt -UserPrompt $unloadPrompt -KeepAliveSeconds 0 -Options $options
  } catch { }
}

$summaryByModel = $results | Group-Object model | ForEach-Object {
  $g = $_.Group
  [pscustomobject]@{
    model = $_.Name
    tests = $g.Count
    pass_rate_pct = [math]::Round((($g | Where-Object {$_.pass}).Count / [double]$g.Count) * 100, 1)
    json_rate_pct = [math]::Round((($g | Where-Object {$_.json_valid}).Count / [double]$g.Count) * 100, 1)
    avg_gen_tok_s = [math]::Round(($g | Measure-Object gen_tok_s -Average).Average, 2)
    avg_total_s = [math]::Round(($g | Measure-Object total_s -Average).Average, 3)
  }
} | Sort-Object -Property pass_rate_pct, avg_gen_tok_s -Descending

$summaryByTest = $results | Group-Object test_id | ForEach-Object {
  $g = $_.Group
  [pscustomobject]@{
    test_id = $_.Name
    runs = $g.Count
    pass_rate_pct = [math]::Round((($g | Where-Object {$_.pass}).Count / [double]$g.Count) * 100, 1)
    json_rate_pct = [math]::Round((($g | Where-Object {$_.json_valid}).Count / [double]$g.Count) * 100, 1)
    avg_total_s = [math]::Round(($g | Measure-Object total_s -Average).Average, 3)
  }
} | Sort-Object test_id

$reportPath = Join-Path $OutDir "report.md"
$csvPath = Join-Path $OutDir "results.csv"
$results | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $csvPath

$md = New-Object System.Collections.Generic.List[string]
$md.Add("# CubeSat Ollama Benchmark")
$md.Add("")
$md.Add("- Fecha: **" + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + "**")
$md.Add("- Endpoint: **" + $endpoint + "**")
$md.Add("- Suite: `"" + $SuiteFile + "`"")
$md.Add("- Modelos: **" + ($Models -join ", ") + "**")
$md.Add("- Repeats por caso: **" + $Repeats + "**")
$md.Add("")
$md.Add("## Resumen por modelo")
$md.Add("")
$md.Add((ToMarkdownTable -Rows $summaryByModel -Columns @("model","tests","pass_rate_pct","json_rate_pct","avg_gen_tok_s","avg_total_s") -Headers @{ model="Modelo"; tests="Corridas"; pass_rate_pct="Pass %"; json_rate_pct="JSON %"; avg_gen_tok_s="Avg gen tok/s"; avg_total_s="Avg total s" }))
$md.Add("")
$md.Add("## Resumen por caso")
$md.Add("")
$md.Add((ToMarkdownTable -Rows $summaryByTest -Columns @("test_id","runs","pass_rate_pct","json_rate_pct","avg_total_s") -Headers @{ test_id="Caso"; runs="Corridas"; pass_rate_pct="Pass %"; json_rate_pct="JSON %"; avg_total_s="Avg total s" }))
$md.Add("")
$md.Add("## Detalle")
$md.Add("")
$md.Add((ToMarkdownTable -Rows $results -Columns @("model","test_id","category","run","pass","json_valid","score","gen_tok_s","total_s") -Headers @{ model="Modelo"; test_id="Caso"; category="Categoría"; run="Run"; pass="Pass"; json_valid="JSON"; score="Score"; gen_tok_s="gen tok/s"; total_s="total s" }))
$md.Add("")
$md.Add("## Archivos")
$md.Add("")
$md.Add("- Reporte CSV: `"" + $csvPath + "`"")
$md.Add("- Respuestas y evaluaciones: `"" + $ResponsesDir + "`"")
$md.Add("")
Save-TextFile -Path $reportPath -Text ($md -join "`r`n")

Write-Host ""
Write-Host ("Reporte generado: " + $reportPath) -ForegroundColor Green
Write-Host ("CSV generado: " + $csvPath) -ForegroundColor Green
Write-Host ("Respuestas en: " + $ResponsesDir) -ForegroundColor Green
