$ErrorActionPreference = "Stop"

$installedDistros = @(& wsl.exe --list --quiet) |
    ForEach-Object { ($_ -replace "`0", "").Trim() } |
    Where-Object { $_ }
if ($LASTEXITCODE -ne 0 -or $installedDistros.Count -eq 0) {
    throw "No WSL distribution is available."
}
$distro = $installedDistros | Where-Object { $_ -match "Ubuntu" } | Select-Object -First 1
if (-not $distro) {
    $distro = $installedDistros[0]
}
$windowsScript = (Join-Path $PSScriptRoot "check-toolchain.sh").Replace("\", "/")
$translatedPath = & wsl.exe -d $distro -- wslpath -a -u $windowsScript
if ($LASTEXITCODE -ne 0 -or -not $translatedPath) {
    throw "Could not translate the toolchain check path for WSL."
}
$linuxScript = $translatedPath.Trim()

& wsl.exe -d $distro -- bash $linuxScript
exit $LASTEXITCODE
