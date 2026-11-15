$token = Read-Host "Enter your Discord bot token"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "Token cannot be empty!"
    exit
}

$scriptsPath = Join-Path $PSScriptRoot "scripts"

if (!(Test-Path $scriptsPath)) {
    New-Item -ItemType Directory -Path $scriptsPath | Out-Null
}

$launcherPath = Join-Path $scriptsPath "start.ps1"

$scriptContent = @"
`$token = "$token"
python ..\src\main.py --token `$token
"@

Set-Content -Path $launcherPath -Value $scriptContent -Encoding UTF8

Write-Host "Launcher generated at: $launcherPath"