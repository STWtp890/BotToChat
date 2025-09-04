@echo off
REM 检查并创建虚拟环境
REM if not exist "Ncatbot_env" (
REM    echo Creating virtual environment...
REM    echo 创建Bot虚拟环境中:
REM    python -m venv Ncatbot_env
REM )
REM 安装依赖并运行脚本的关键：在同一上下文中依次执行
REM 使用 call 命令运行激活脚本，然后执行后续命令
call Ncatbot_env\Scripts\activate.bat && (
    echo Installing dependencies from requirements.txt...
    echo 从requirements.txt中安装软件包依赖:
    pip install -r requirements.txt
    python your_script.py
)
pause