@echo off
rem ============================================================
rem  Verfjes data - start de web app en opent direct je browser
rem  Dubbelklik op dit bestand om te starten.
rem ============================================================
title Verfjes data
cd /d "%~dp0"

rem Controleer of Python en Streamlit geinstalleerd zijn
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is niet geinstalleerd of niet gevonden!
    echo Installeer Python van https://www.python.org/downloads/ en probeer opnieuw.
    pause
    exit /b 1
)

python -m streamlit run src\app.py
pause
