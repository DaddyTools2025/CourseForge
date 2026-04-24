@echo off
chcp 65001 >nul
title CourseForge 铸课工坊 - 启动器

echo ========================================
echo   CourseForge 铸课工坊 v2.0
echo   一键启动程序
echo ========================================
echo.

REM 检查 Python 版本
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 错误: 未检测到 Python
    echo [i] 请先安装 Python 3.9 或更高版本
    echo [i] 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python 版本: %PYTHON_VERSION%

REM 检查虚拟环境
echo.
echo [2/4] 检查虚拟环境...
if not exist "venv\" (
    echo [i] 未检测到虚拟环境，正在创建...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo [+] 虚拟环境创建成功
) else (
    echo [+] 虚拟环境已存在
)

REM 激活虚拟环境
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [!] 虚拟环境激活失败
    pause
    exit /b 1
)

REM 检查依赖包
echo.
echo [3/4] 检查依赖包...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [i] 检测到缺少依赖包，正在安装...
    echo [i] 这可能需要几分钟时间，请耐心等待...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo [!] 依赖包安装失败
        echo [i] 尝试使用默认源重新安装...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            pause
            exit /b 1
        )
    )
    echo [+] 依赖包安装成功
) else (
    echo [+] 依赖包已安装
)

REM 启动应用
echo.
echo [4/4] 启动 CourseForge...
echo [+] 浏览器将自动打开应用界面
echo [i] 按 Ctrl+C 可停止程序
echo.
streamlit run app.py

REM 退出时提示
echo.
echo ========================================
echo   程序已停止运行
echo ========================================
pause
