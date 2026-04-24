#!/bin/bash

# CourseForge 快捷方式安装脚本
# 自动在桌面生成图标

APP_NAME="CourseForge 铸课工坊"
APP_DIR=$(pwd)
ICON_PATH="$APP_DIR/assets/icon.png" # 假设有个图标，如果没有也没关系，会用默认图标
EXEC_PATH="$APP_DIR/start.sh"

# 检查 start.sh 是否有执行权限
chmod +x "$EXEC_PATH"

# 获取桌面路径
DESKTOP_DIR="$HOME/Desktop"
if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="$HOME/桌面"
fi

# 如果桌面目录不存在，尝试标准 XDG 目录
if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR=$(xdg-user-dir DESKTOP 2>/dev/null)
fi

# 如果还是找不到，就放在当前目录
if [ -z "$DESKTOP_DIR" ] || [ ! -d "$DESKTOP_DIR" ]; then
    echo "未找到桌面目录，将在当前目录生成快捷方式"
    DESKTOP_DIR="$APP_DIR"
fi

SHORTCUT_FILE="$DESKTOP_DIR/CourseForge.desktop"

echo "正在生成快捷方式: $SHORTCUT_FILE"

cat > "$SHORTCUT_FILE" << EOF
[Desktop Entry]
Name=$APP_NAME
Comment=AI 备课助手
Exec="$EXEC_PATH"
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Education;Office;
EOF

chmod +x "$SHORTCUT_FILE"

echo "========================================"
echo "✅ 快捷方式已创建！"
echo "📍 位置: $SHORTCUT_FILE"
echo "👉 您现在可以直接双击该图标启动程序"
echo "========================================"
echo ""
read -p "按回车键退出..."
