@echo off
REM ===========================================================================
REM  IA Locale - Installation Cle en Main V2 (double-clic)
REM  Nouveau flux : Diagnostic -> Install tout -> Re-diagnostic
REM ===========================================================================
title IA Locale - Installation V2 Cle en Main
cd /d "%~dp0"
echo ======================================================================
echo   IA LOCALE - INSTALLATION CLE EN MAIN V2
echo   Diagnostic -> Telechargement composants -> Re-diagnostic
echo ======================================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL.ps1" %*
pause
