$ProgressPreference='SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
'start ' + $(Get-Date) | Out-File 'C:\Users\amanu\.cline\data\workspaces\chat\_dl.txt' -Encoding utf8
try {
  Invoke-WebRequest -Uri 'https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip' -OutFile 'C:\Users\amanu\flutter_sdk.zip' -TimeoutSec 1800
  'zip bytes: ' + (Get-Item 'C:\Users\amanu\flutter_sdk.zip').Length | Out-File 'C:\Users\amanu\.cline\data\workspaces\chat\_dl.txt' -Append -Encoding utf8
} catch {
  'DOWNLOAD FAILED: ' + $_.Exception.Message | Out-File 'C:\Users\amanu\.cline\data\workspaces\chat\_dl.txt' -Append -Encoding utf8
  exit 1
}
Remove-Item 'C:\Users\amanu\flutter' -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive -LiteralPath 'C:\Users\amanu\flutter_sdk.zip' -DestinationPath 'C:\Users\amanu' -Force
'extracted; bin=' + (Test-Path 'C:\Users\amanu\flutter\bin\flutter.bat') | Out-File 'C:\Users\amanu\.cline\data\workspaces\chat\_dl.txt' -Append -Encoding utf8
Remove-Item 'C:\Users\amanu\flutter_sdk.zip' -Force -ErrorAction SilentlyContinue
'done ' + $(Get-Date) | Out-File 'C:\Users\amanu\.cline\data\workspaces\chat\_dl.txt' -Append -Encoding utf8
