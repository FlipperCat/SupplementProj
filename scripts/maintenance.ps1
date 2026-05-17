#requires -Version 5.1
<#
.SYNOPSIS
  VitaWise daily maintenance. Pulls latest, crawls live site, invokes
  Claude headless to fix any broken links, pushes if changes were made.

.NOTES
  Runs from Windows Task Scheduler. No interactive prompts. All output is
  appended to .maintenance/<date>.log next to the repo root.
#>

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\altst\supplement-guide'
$logDir = Join-Path $repo '.maintenance'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$today = Get-Date -Format yyyy-MM-dd
$log = Join-Path $logDir "$today.log"

function Log {
    param([string]$msg)
    $line = "[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $msg
    Add-Content -Path $log -Value $line -Encoding utf8
    Write-Host $line
}

Set-Location $repo

Log '=== VitaWise daily maintenance run ==='
Log "Repo: $repo"

# Refuse to run if user hasn't authorized subscription mode (no API key)
if ($env:ANTHROPIC_API_KEY) {
    Log 'ABORT: ANTHROPIC_API_KEY is set; this account is subscription-only.'
    exit 1
}

# 1. Pull
Log 'git pull --rebase origin main'
$pullOutput = git pull --rebase origin main 2>&1 | Out-String
Add-Content -Path $log -Value $pullOutput -Encoding utf8

# 2. Crawl pre-state to baseline (informational)
Log 'crawl: pre-fix baseline'
$preCrawl = python -X utf8 scripts/crawl.py 2>&1 | Out-String
Add-Content -Path $log -Value $preCrawl -Encoding utf8
$preBroken = ($preCrawl | Select-String -Pattern 'Broken:\s+(\d+)').Matches.Groups[1].Value
Log "pre-fix broken: $preBroken"

if ([int]$preBroken -eq 0) {
    Log "OK $today: 0 broken links, nothing to do."
    exit 0
}

# 3. Invoke Claude headless to triage + fix
Log "Invoking claude headless with /audit (preBroken=$preBroken)..."
$claudeOutput = & claude -p '/audit' --output-format text --dangerously-skip-permissions 2>&1 | Out-String
Add-Content -Path $log -Value '--- claude /audit output ---' -Encoding utf8
Add-Content -Path $log -Value $claudeOutput -Encoding utf8
Add-Content -Path $log -Value '--- end claude output ---' -Encoding utf8

# 4. Post-fix crawl
Log 'crawl: post-fix verify'
$postCrawl = python -X utf8 scripts/crawl.py 2>&1 | Out-String
Add-Content -Path $log -Value $postCrawl -Encoding utf8
$postBroken = ($postCrawl | Select-String -Pattern 'Broken:\s+(\d+)').Matches.Groups[1].Value

Log "result: pre=$preBroken  post=$postBroken"

if ([int]$postBroken -lt [int]$preBroken) {
    Log "Improved: -$([int]$preBroken - [int]$postBroken) broken links."
} elseif ([int]$postBroken -gt 0) {
    Log "STILL BROKEN: $postBroken links unresolved (claude couldn't autofix all). Check log + Obsidian Ideas/ folder."
}

Log '=== run complete ==='

# 5. Link-graph audit (read-only; warn if any supplement page is under-linked)
$logDir = Join-Path $PSScriptRoot "..\.maintenance"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir ("link-graph-" + (Get-Date -Format "yyyy-MM-dd") + ".md")
python (Join-Path $PSScriptRoot "check_link_graph.py") --report-md $logFile
if ($LASTEXITCODE -ne 0) { Write-Warning "Link-graph audit found failing pages -- see $logFile" }
