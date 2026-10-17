@echo off
setlocal
cd /d "%~dp0"

where node >nul 2>&1
if errorlevel 1 (
  echo Node.js nao encontrado no PATH. Instale em https://nodejs.org
  echo.
  pause
  exit /b 1
)

node scripts\app.mjs status
echo.
pause
endlocal
