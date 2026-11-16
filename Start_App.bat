@echo off
setlocal EnableExtensions
rem ============================================================
rem  Verfjes data - launcher
rem  - Checkt of Python en de benodigde pakketten aanwezig zijn
rem  - Installeert ontbrekende onderdelen automatisch
rem  - Start de web app en opent de browser
rem  Dubbelklik op dit bestand om te starten.
rem ============================================================
title Verfjes data
cd /d "%~dp0"

rem --- Zoek Python ---------------------------------------------
set "PYTHON_EXE="
where python >nul 2>&1 && set "PYTHON_EXE=python"
if not defined PYTHON_EXE (
    where py >nul 2>&1 && set "PYTHON_EXE=py -3"
)

rem --- Python ontbreekt: download en installeer automatisch ----
if not defined PYTHON_EXE (
    echo Python is niet geinstalleerd. Download en installatie start nu...
    set "PYVER=3.13.5"
    set "PYSETUP=%TEMP%\python-%PYVER%-amd64.exe"
    powershell -NoProfile -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-amd64.exe -OutFile %PYSETUP%"
    if errorlevel 1 (
        echo.
        echo Downloaden van Python is mislukt.
        echo Installeer handmatig Python van https://www.python.org/downloads/
        echo en start dit bestand opnieuw.
        pause
        exit /b 1
    )
    start /wait "" "%PYSETUP%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del /q "%PYSETUP%" >nul 2>&1
    rem Ververs PATH met de locatie van een user-installatie
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python313") do (
        set "PATH=%%D;%%D\Scripts;%PATH%"
    )
    where python >nul 2>&1 && set "PYTHON_EXE=python"
    if not defined PYTHON_EXE (
        echo.
        echo Python-installatie is niet geslaagd.
        echo Herstart de computer en probeer het opnieuw, of installeer Python handmatig.
        pause
        exit /b 1
    )
    echo Python is geinstalleerd.
)

rem --- Pakketten (Streamlit, pandas, openpyxl) ------------------
%PYTHON_EXE% -c "import streamlit, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Benodigde Python-pakketten worden geinstalleerd, dit kan even duren...
    %PYTHON_EXE% -m pip install --upgrade pip >nul
    %PYTHON_EXE% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Installatie van de pakketten is mislukt.
        echo Controleer de internetverbinding en probeer het opnieuw.
        pause
        exit /b 1
    )
    echo Pakketten zijn geinstalleerd.
)

rem --- Start de web app ------------------------------------------
%PYTHON_EXE% -m streamlit run src\app.py
pause
