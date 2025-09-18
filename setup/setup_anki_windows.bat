@echo off
echo Setting up Anki for remote access...
echo.

echo Setting environment variable...
set ANKICONNECT_BIND_ADDRESS=0.0.0.0

echo.
echo Environment variable set. Now starting Anki...
echo Keep this window open while using the Codespace integration.
echo.

REM Try to find and start Anki
if exist "C:\Program Files\Anki\anki.exe" (
    start "Anki" "C:\Program Files\Anki\anki.exe"
) else if exist "C:\Program Files (x86)\Anki\anki.exe" (
    start "Anki" "C:\Program Files (x86)\Anki\anki.exe"
) else (
    echo Could not find Anki automatically.
    echo Please start Anki manually from this command prompt window.
    echo.
)

echo.
echo Find your IP address with: ipconfig | findstr "IPv4"
ipconfig | findstr "IPv4"

echo.
echo Use the IP address shown above in your Codespace setup.
pause
