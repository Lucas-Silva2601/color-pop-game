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

rem Passa argumentos extras, ex.: start.bat --prod ou start.bat --port 4000
node scripts\app.mjs start %*

if errorlevel 1 (
  echo.
  pause
) else (
  timeout /t 2 /nobreak >nul 2>&1
)
endlocal
