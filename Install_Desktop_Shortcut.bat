@echo off
title Install J.A.R.V.I.S. Desktop Shortcut
cd /d "%~dp0"
echo ========================================================
echo       INSTALLING J.A.R.V.I.S. DESKTOP SHORTCUT
echo ========================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_shortcut.ps1"
echo.
echo [*] Shortcut created on your Desktop with the Arc Reactor logo!
echo [*] You can now double-click "J.A.R.V.I.S." on your Desktop anytime.
echo.
pause

