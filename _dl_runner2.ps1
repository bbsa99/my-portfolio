$ErrorActionPreference = 'Continue'
$log = 'C:\Users\amanu\.cline\data\workspaces\chat\_dl2.txt'
$url = 'https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip'
$zip = 'C:\Users\amanu\flutter_sdk.zip'
$expected = 1934624561
function L($m){ $m | Out-File $log -Append -Encoding utf8 }

Remove-Item $log -ErrorAction SilentlyContinue
L ('dl2 start ' + (Get-Date) + ' ; expectedMB=' + [math]::Round($expected/1MB))

$attempt = 0
while($true){
  $attempt++
  $cur = 0
  if(Test-Path $zip){ $cur = (Get-Item $zip).Length }
  L ("attempt=$attempt currentMB=" + [math]::Round($cur/1MB))
  if($cur -ge $expected){ L 'SIZE_REACHED'; break }
  if($attempt -gt 400){ L 'TOO_MANY_ATTEMPTS'; break }

  # Resume-capable download; give up if stalled so the loop can retry.
  & curl.exe -L -C - --retry 8 --retry-delay 5 --retry-all-errors --retry-connrefused `
      --connect-timeout 30 --speed-limit 2048 --speed-time 45 `
      -o "$zip" "$url" 2>&1 | Out-File $log -Append -Encoding utf8
  L ('  curl_exit=' + $LASTEXITCODE + ' at ' + (Get-Date).ToString('HH:mm:ss'))
  Start-Sleep -Seconds 3
}

$final = 0
if(Test-Path $zip){ $final = (Get-Item $zip).Length }
L ('finalMB=' + [math]::Round($final/1MB))

if($final -ge $expected){
  L 'extracting...'
  Remove-Item 'C:\Users\amanu\flutter' -Recurse -Force -ErrorAction SilentlyContinue
  Expand-Archive -LiteralPath $zip -DestinationPath 'C:\Users\amanu' -Force
  L ('extracted bin=' + (Test-Path 'C:\Users\amanu\flutter\bin\flutter.bat'))
  Remove-Item $zip -Force -ErrorAction SilentlyContinue

  $env:Path = 'C:\Users\amanu\flutter\bin;' + $env:Path
  L '--- flutter --version (downloads Dart engine on first run) ---'
  & flutter --version 2>&1 | Out-File $log -Append -Encoding utf8
  L ('version_exit=' + $LASTEXITCODE)
  L '--- config enable-web ---'
  & flutter config --enable-web --no-analytics 2>&1 | Out-File $log -Append -Encoding utf8
  L '--- pub get ---'
  Set-Location 'C:\Users\amanu\.cline\data\workspaces\chat\yonas project\TaxiMeter_Flutter'
  & flutter pub get 2>&1 | Out-File $log -Append -Encoding utf8
  L ('pubget_exit=' + $LASTEXITCODE)
  L ('ALL_DONE ' + (Get-Date))
} else {
  L 'INCOMPLETE_NOT_EXTRACTED'
}
