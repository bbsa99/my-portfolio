$npmPath = "C:\Program Files\nodejs\npm.exe"
$wsPath = "C:\Users\amanu\.cline\data\workspaces\chat\joy-massage-spa"
if (Test-Path $npmPath) {
    Set-Location $wsPath
    & $npmPath install
} else {
    Write-Host "npm not found at expected path"
}