@echo off
setlocal enabledelayedexpansion

echo Please enter the parent folder path (Leave blank to use the location of this batch file):
set /p parentPath=

if "%parentPath%"=="" set parentPath=%~dp0

echo Please enter the start number:
set /p startNum=

echo Please enter the end number:
set /p endNum=

for /L %%i in (%startNum%, 1, %endNum%) do (
    mkdir "%parentPath%\%%i"
    echo Created folder %%i in %parentPath%
)

echo All folders from %startNum% to %endNum% have been created in %parentPath%!
pause
