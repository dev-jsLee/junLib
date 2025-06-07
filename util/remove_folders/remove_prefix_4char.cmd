@echo off
setlocal enabledelayedexpansion
:start
cls
set /p "folder=input folder path: "

for %%F in ("%folder%\*") do (
    set "filename=%%~nxF"
    set "newname=!filename:~4!"
    ren "%%F" "!newname!"
)

echo 파일명의 앞 4글자를 삭제했습니다.
pause
goto start