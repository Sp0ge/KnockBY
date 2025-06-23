@echo off
chcp 1251 > nul
SETLOCAL

echo .
echo ██╗  ██╗███╗   ██╗ ██████╗ ███╗   ██╗██╗  ██╗    ██████╗ ██╗   ██╗
echo ██║ ██╔╝████╗  ██║██╔═══██╗████╗  ██║██║ ██╔╝    ██╔══██╗╚██╗ ██╔╝
echo █████╔╝ ██╔██╗ ██║██║   ██║██╔██╗ ██║█████╔╝     ██████╔╝ ╚████╔╝ 
echo ██╔═██╗ ██║╚██╗██║██║   ██║██║╚██╗██║██╔═██╗     ██╔══██╗  ╚██╔╝  
echo ██║  ██╗██║ ╚████║╚██████╔╝██║ ╚████║██║  ██╗    ██████╔╝   ██║   
echo ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝    ╚═╝   
echo .

for /f "tokens=2 delims==" %%P in ('python --version 2^>^&1') do (
    for /f "tokens=1,2 delims=." %%A in ("%%P") do (
        if %%A LSS 3 (
            echo Error: Python 3.7+ required
            echo Please install Python 3.7+ and add to PATH
            pause
            exit /b 1
        )
        if %%A EQU 3 if %%B LSS 7 (
            echo Error: Found Python %%A.%%B, required 3.7+
            echo Please install Python 3.7+ and add to PATH
            pause
            exit /b 1
        )
    )
)

if exist venv (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

echo Creating new virtual environment...
python3.12 -m venv venv

echo Installing dependencies from requirements.txt...
call venv\Scripts\activate
pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found
    pause
    exit /b 1
)

if exist KnockBy (
    cd KnockBy
    echo Starting KnockBy.py...
    python KnockBy.py
) else (
    echo KnockBy folder not found
    pause
    exit /b 1
)

pause
ENDLOCAL