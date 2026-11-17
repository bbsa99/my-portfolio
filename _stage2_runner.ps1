$ErrorActionPreference='Continue'
$log='C:\Users\amanu\.cline\data\workspaces\chat\_stage2.txt'
function L($m){ $m | Out-File $log -Append -Encoding utf8 }
L ('stage2 start ' + (Get-Date))
# wait for flutter.bat (download + extract)
$i=0
while(-not (Test-Path 'C:\Users\amanu\flutter\bin\flutter.bat') -and $i -lt 240){
  Start-Sleep -Seconds 15; $i++
  if(($i % 4) -eq 0){ L ('waiting for sdk... ' + $i*15 + 's; zipMB=' + $(if(Test-Path 'C:\Users\amanu\flutter_sdk.zip'){[math]::Round((Get-Item 'C:\Users\amanu\flutter_sdk.zip').Length/1MB)}else{'extracted?'})) }
}
if(-not (Test-Path 'C:\Users\amanu\flutter\bin\flutter.bat')){ L 'SDK NEVER APPEARED'; exit 1 }
L ('sdk ready ' + (Get-Date))
$env:Path = 'C:\Users\amanu\flutter\bin;' + $env:Path
L '--- flutter --version (first run downloads Dart engine) ---'
flutter --version 2>&1 | Out-File $log -Append -Encoding utf8
L '--- config enable-web ---'
flutter config --enable-web --no-analytics 2>&1 | Out-File $log -Append -Encoding utf8
L '--- pub get ---'
Set-Location 'C:\Users\amanu\.cline\data\workspaces\chat\yonas project\TaxiMeter_Flutter'
flutter pub get 2>&1 | Out-File $log -Append -Encoding utf8
L ('stage2 done ' + (Get-Date))
