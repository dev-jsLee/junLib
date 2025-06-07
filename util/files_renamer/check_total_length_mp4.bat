@echo off

REM moviepy 패키지 설치 여부 확인
pip show moviepy > nul 2>&1
if %errorlevel% neq 0 (
    echo "moviepy 패키지가 설치되지 않았습니다. 자동으로 설치합니다..."
    pip install moviepy
    if %errorlevel% neq 0 (
        echo "moviepy 패키지 설치 중 오류가 발생했습니다."
        pause
        exit /b
    )
    echo "moviepy 패키지가 성공적으로 설치되었습니다."
)

REM Python 스크립트 실행
python main.py

pause
