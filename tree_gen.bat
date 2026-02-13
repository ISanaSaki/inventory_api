@echo off
REM Generates a cleaned tree.txt in the current directory

set "OUT=tree.txt"

REM Call PowerShell to build a filtered tree
powershell -NoLogo -NoProfile -Command ^
  "$excluded = @('.venv','venv','env','__pycache__','.pytest_cache','.git','Lib','Include','Scripts','site-packages','dist-info','etc');" ^
  "function Show-Tree([string]$path='.', [string]$prefix='') {" ^
  "  Get-ChildItem -LiteralPath $path | Where-Object {" ^
  "    $name = $_.Name; -not ($excluded -contains $name)" ^
  "  } | ForEach-Object {" ^
  "    $item = $_;" ^
  "    if ($item.PSIsContainer) {" ^
  "      Write-Output ($prefix + '|-- ' + $item.Name);" ^
  "      Show-Tree -path $item.FullName -prefix ($prefix + '    ')" ^
  "    } else {" ^
  "      Write-Output ($prefix + '|-- ' + $item.Name)" ^
  "    }" ^
  "  }" ^
  "};" ^
  "Show-Tree | Out-File -Encoding utf8 $env:OUT"

echo Created %OUT% in %CD%
echo.

REM ============================================
REM =============== DONE ASCII =================
REM ============================================
REM Enable ANSI escape sequences
for /f "delims=" %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

set "GREEN=%ESC%[92m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

echo %CYAN% DDDDD    oooooo  NNN    NN EEEEEEE%GREEN%
echo %CYAN% D   DD  o      o NNNN   NN EE     %GREEN%
echo %CYAN% D    D  o      o NN NN  NN EEEEE  %GREEN%
echo %CYAN% D   DD  o      o NN  NN NN EE     %GREEN%
echo %CYAN% DDDDD    oooooo  NN   NNNN EEEEEEE%GREEN%
echo.
echo %GREEN%==================== DONE ====================%RESET%
echo.

pause
