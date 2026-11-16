@echo off
setlocal EnableExtensions
rem ============================================================
rem  Verfjes data - launcher
rem  - Checkt of Python en de benodigde pakketten aanwezig zijn
rem  - Negeert de Microsoft Store-aliases van Windows (nep python.exe)
rem  - Installeert ontbrekende onderdelen automatisch
rem  - Start de web app en opent de browser
rem  Dubbelklik op dit bestand om te starten.
rem ============================================================
title Verfjes data
cd /d "%~dp0"

rem --- Zoek een ECHTE Python (Microsoft Store-alias overslaan) --
rem Windows 11 legt een nep python.exe in WindowsApps dat de
rem Microsoft Store opent. Die mag hier NIET als Python tellen.
set "PYCMD="
for /f "delims=" %%P in ('where python 2^>nul') do (
    echo %%P | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        if not defined PYCMD set "PYCMD=%%P"
    )
)
if not defined PYCMD (
    for /f "delims=" %%P in ('where py 2^>nul') do (
        echo %%P | findstr /i "WindowsApps" >nul
        if errorlevel 1 (
            if not defined PYCMD set "PYCMD=py -3"
        )
    )
)

rem --- Python ontbreekt: download en installeer automatisch ----
if not defined PYCMD (
    echo Python is niet geinstalleerd. Download en installatie start nu...
    set "PYVER=3.13.5"
    set "PYSETUP=%TEMP%\python-%PYVER%-amd64.exe"
    echo Download: https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-amd64.exe
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-amd64.exe -OutFile '%PYSETUP%'"
    if not exist "%PYSETUP%" (
        echo Download via PowerShell is mislukt, probeer met curl...
        curl -sL -o "%PYSETUP%" https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-amd64.exe
    )
    if not exist "%PYSETUP%" (
        echo.
        echo Downloaden van Python is mislukt.
        echo Installeer handmatig Python van https://www.python.org/downloads/
        echo en start dit bestand opnieuw.
        pause
        exit /b 1
    )
    start /wait "" "%PYSETUP%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del /q "%PYSETUP%" >nul 2>&1
    rem Gebruik direct de geinstalleerde locatie (veelbetrouwbaarder dan PATH)
    if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
        set "PYCMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    )
    if not defined PYCMD (
        for /f "delims=" %%P in ('where python 2^>nul') do (
            echo %%P | findstr /i "WindowsApps" >nul
            if errorlevel 1 (
                if not defined PYCMD set "PYCMD=%%P"
            )
        )
    )
    if not defined PYCMD (
        echo.
        echo Python-installatie is niet geslaagd.
        echo Herstart de computer en probeer het opnieuw, of installeer Python handmatig.
        pause
        exit /b 1
    )
    echo Python is geinstalleerd.
)

rem --- Koppel het correcte aanroep-opdracht (path met spaties = citeren) --
set "PY="
echo %PYCMD% | findstr /i ".exe" >nul
if not errorlevel 1 (
    set "PY="%PYCMD%""
) else (
    set "PY=%PYCMD%"
)

rem --- Pakketten (Streamlit, pandas, openpyxl) ------------------
%PY% -c "import streamlit, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Benodigde Python-pakketten worden geinstalleerd, dit kan even duren...
    %PY% -m pip install --upgrade pip >nul
    %PY% -m pip install -r requirements.txt
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
%PY% -m streamlit run src\app.py
pause