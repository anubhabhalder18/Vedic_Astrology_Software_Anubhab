# -------------------------------------------------------------
#  Cairo Auto Installer for Windows
#  Installs MSYS2 + Cairo DLLs + Updates PATH
# -------------------------------------------------------------


Write-Host "==============================================="
Write-Host "       Installing Cairo DLL for Windows"
Write-Host "==============================================="


# 1) Download MSYS2 Installer
$msys_url = "https://repo.msys2.org/distrib/x86_64/msys2-x86_64-latest.exe"
$installer = "$env:TEMP\msys2_installer.exe"

Write-Host "Downloading MSYS2 installer..."
Invoke-WebRequest -Uri $msys_url -OutFile $installer


# 2) Install MSYS2 silently
$msys_dir = "C:\msys64"

if (Test-Path $msys_dir) {
    Write-Host "MSYS2 already installed."
} else {
    Write-Host "Installing MSYS2..."
    Start-Process -FilePath $installer -ArgumentList "/S" -Wait
}


# 3) Run MSYS2 update and install Cairo
Write-Host "Updating MSYS2 and installing Cairo..."
$pacman = "$msys_dir\usr\bin\bash.exe"

Start-Process $pacman -ArgumentList "-lc `"pacman -Syu --noconfirm`"" -Wait
Start-Process $pacman -ArgumentList "-lc `"pacman -S mingw-w64-x86_64-cairo --noconfirm`"" -Wait


# 4) Add Cairo DLL path to Windows PATH
$cairo_path = "C:\msys64\mingw64\bin"

Write-Host "Adding Cairo DLL path to system PATH..."
$env_path = [Environment]::GetEnvironmentVariable("Path", "Machine")

if ($env_path -notlike "*$cairo_path*") {
    $new_path = "$env_path;$cairo_path"
    Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment -Name Path -Value $new_path
    Write-Host "✔ Cairo path added to PATH."
} else {
    Write-Host "✔ Cairo path already exists."
}


# 5) Done
Write-Host "==============================================="
Write-Host "   Cairo installation completed successfully!"
Write-Host "   RESTART YOUR PC for PATH to update."
Write-Host "==============================================="
