# 设置UTF-8编码
$OutputEncoding = New-Object -typename System.Text.UTF8Encoding

# 检查Python版本
Write-Host "Checking Python version..."
python --version >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed. Please install Python and try again."
    Write-Host "请安装Python并重新运行脚本."
    pause
    exit 1
}

# 检查并创建虚拟环境
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    Write-Host "创建Bot虚拟环境中:"
    python -m venv .venv
}

# 检查虚拟环境是否创建成功
if (!(Test-Path ".venv")) {
    Write-Host "Failed to create virtual environment."
    Write-Host "创建虚拟环境失败."
    pause
    exit 1
}

# 激活虚拟环境并安装依赖
Write-Host "Activating virtual environment..."
.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment."
    Write-Host "激活虚拟环境失败."
    pause
    exit 1
}

Write-Host "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies."
    Write-Host "安装依赖失败."
    pause
    exit 1
}

Write-Host "Starting the Python script:"
Write-Host "启动Python脚本:"
python run.py
pause
