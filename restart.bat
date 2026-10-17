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

rem Reinicia no mesmo modo (dev ou producao) em que estava rodando.
node scripts\app.mjs restart %*

if errorlevel 1 (
  echo.
  pause
) else (
  timeout /t 2 /nobreak >nul 2>&1
)
endlocal
