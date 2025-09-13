@echo off
REM 使用UTF-8编码
chcp 65001 >nul

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python and try again.
    echo 请安装Python并重新运行脚本.
    pause
    exit /b 1
)

REM 检查并创建虚拟环境
if not exist ".venv" (
    echo Creating virtual environment...
    echo 创建Bot虚拟环境中:
    python -m venv .venv
)

REM 检查虚拟环境是否创建成功
if not exist ".venv" (
    echo Failed to create virtual environment.
    echo 创建虚拟环境失败.
    pause
    exit /b 1
)

REM 激活虚拟环境并安装依赖
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    echo 激活虚拟环境失败.
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo 安装依赖失败.
    pause
    exit /b 1
)

echo Starting the Python script:
echo 启动Python脚本:
python run.py
pause
