@echo off
set /p target_path="Enter target folder path: "

for /r "%target_path%" %%f in (*) do (
    move "%%f" "%target_path%\"
)

echo All files have been moved successfully.
pause
