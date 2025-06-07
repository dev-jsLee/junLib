@echo off
setlocal enabledelayedexpansion
cd /d %~dp0
set /p "source_folder=Enter folder path: "
if "%source_folder%"=="" (
    set "source_folder=%CD%"
)

for /R "%source_folder%" %%F in (*.*) do (
    set "file=%%~nxF"
    set "filename=!file:~0,3!"

    rem echo !filename!| findstr /r "^[0-9][0-9][0-9]$"
    if !errorlevel! equ 0 (
        set "folder_number=!filename!"
        set "folder_path=!source_folder!\!folder_number!"

        if not exist "!folder_path!" (
            mkdir "!folder_path!"
        )

        move "%%F" "!folder_path!"
    )
)

echo 작업이 완료되었습니다.
pause
