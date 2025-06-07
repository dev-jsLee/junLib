@echo off
setlocal

set /p "folder_path=Enter folder path: "
if "%folder_path%"=="" (
    set "folder_path=%CD%"
)
cls
python count_images.py "%folder_path%" > count_output.txt

pause

set total_count=0
for /f "tokens=*" %%a in ('type count_output.txt ^| sort /r') do (
    for /f "tokens=*" %%b in ("%%a") do (
        for %%c in (%%b) do (
            echo %%c
            set /a total_count+=%%c
            goto :continue
        )
        :continue
    )
)

echo Total Count: %total_count%
echo Total Count: %total_count% >> count_output.txt

pause
