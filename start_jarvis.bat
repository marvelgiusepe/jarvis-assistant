@echo off
title J.A.R.V.I.S. Autonomous Assistant
cd /d "%~dp0"
echo ========================================================
echo         J.A.R.V.I.S. WORKSTATION CO-PILOT
echo ========================================================
echo [*] Starting local bridge on http://localhost:8765 ...
start http://localhost:8765
python server.py
pause

