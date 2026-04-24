#!/bin/bash

# CourseForge 启动脚本 v2.5
# 支持自动检查和安装依赖
# 适配信创/Linux 桌面环境

echo "========================================"
echo "  CourseForge 铸课工坊 v2.5"
echo "  一键启动程序"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 错误处理函数
handle_error() {
    echo -e "${RED}[!] 发生错误: $1${NC}"
    echo ""
    read -p "按回车键退出..."
    exit 1
}

# 1. 检查 Python 环境
echo "[1/4] 检查 Python 环境..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    handle_error "未检测到 Python。请先安装 Python 3.9+ (sudo apt install python3)"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[+] Python 版本: $PYTHON_VERSION${NC}"

# 2. 检查虚拟环境模块
# 在某些发行版中，venv 是单独的包
$PYTHON_CMD -c "import venv" &> /dev/null
if [ $? -ne 0 ]; then
    handle_error "缺少 venv 模块。请安装 python3-venv (示例: sudo apt install python3-venv)"
fi

# 3. 检查/创建虚拟环境
echo ""
echo "[2/4] 检查虚拟环境..."

if [ ! -d "venv" ]; then
    echo "[i] 未检测到虚拟环境，正在创建..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        handle_error "虚拟环境创建失败。请检查目录权限。"
    fi
    echo -e "${GREEN}[+] 虚拟环境创建成功${NC}"
else
    echo -e "${GREEN}[+] 虚拟环境已存在${NC}"
fi

# 激活虚拟环境
source venv/bin/activate
if [ $? -ne 0 ]; then
    handle_error "虚拟环境激活失败"
fi

# 4. 检查依赖包
echo ""
echo "[3/4] 检查依赖包..."

python -c "import streamlit; import requests; import anthropic; import google.generativeai" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[i] 检测到依赖缺失或更新，正在安装...${NC}"
    
    # 尝试使用国内镜像源（清华源）
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if [ $? -ne 0 ]; then
        echo "[i] 清华源安装失败，尝试官方源..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            handle_error "依赖包安装失败。如果是内网环境，请确保配置了 pip 镜像或离线源。"
        fi
    fi
    echo -e "${GREEN}[+] 依赖包准备就绪${NC}"
else
    echo -e "${GREEN}[+] 所有依赖已就绪${NC}"
fi

# 5. 启动应用
echo ""
echo "[4/4] 启动 CourseForge..."
echo -e "${GREEN}[+] 浏览器将自动打开...${NC}"
echo -e "${YELLOW}[i] 服务运行中，关闭此窗口将停止服务${NC}"
echo ""

# 使用 streamlit run 启动
streamlit run app.py --browser.serverAddress localhost --server.enableCORS false --browser.gatherUsageStats false

# 退出提示
echo ""
echo "========================================"
echo "  程序已停止"
echo "========================================"
read -p "按回车键退出..."
