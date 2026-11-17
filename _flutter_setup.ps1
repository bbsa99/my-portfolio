$ErrorActionPreference = 'Stop'
$flutterBin = 'C:\Users\amanu\flutter\bin'
$env:Path = $flutterBin + ';' + $env:Path
$proj = 'C:\Users\amanu\.cline\data\workspaces\chat\yonas project\TaxiMeter_Flutter'
Set-Location $proj
Write-Host "=== flutter --version ==="
& flutter --version
Write-Host "=== config enable-web ==="
& flutter config --enable-web --no-analytics
Write-Host "=== pub get ==="
& flutter pub get
Write-Host "=== SETUP_DONE ==="
