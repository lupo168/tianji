#!/bin/bash
# 天玑 · 一行命令启动器
# 小白用法: 打开终端, 粘贴这一行, 回车:
#
#   curl -fsSL https://raw.githubusercontent.com/lupo168/tianji/main/quickstart.sh | bash
#
# 自动完成: 检查环境 → 下载代码 → 首次采集 → 生成日报 → 设置定时任务

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}  🌍 天玑 · 全球商业情报系统${NC}"
echo -e "${BLUE}  ===========================${NC}"
echo ""

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}  ❌ 未找到 Python3${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  💡 请先安装 Homebrew:"
        echo "     /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "  💡 然后安装 Python:"
        echo "     brew install python3"
    else
        echo "  💡 安装: sudo apt install python3 python3-pip"
    fi
    exit 1
fi

echo -e "${GREEN}  ✅ Python: $(python3 --version)${NC}"

# 2. 克隆/更新仓库
REPO_DIR="$HOME/tianji"
if [ -d "$REPO_DIR" ]; then
    echo -e "${BLUE}  📦 更新天玑...${NC}"
    cd "$REPO_DIR" && git pull --quiet
else
    echo -e "${BLUE}  📦 下载天玑...${NC}"
    git clone --quiet https://github.com/lupo168/tianji.git "$REPO_DIR"
fi
echo -e "${GREEN}  ✅ 代码就绪: $REPO_DIR${NC}"

# 3. 创建数据目录
echo -e "${BLUE}  📁 创建数据目录...${NC}"
mkdir -p ~/tianji-data/{exchange-rates,news,trends,hackernews,government,commodities,reports,daily-logs}
echo -e "${GREEN}  ✅ 数据目录: ~/tianji-data/${NC}"

# 4. 首次采集运行
echo -e "${BLUE}  🚀 首次采集 (约30秒)...${NC}"
cd "$REPO_DIR/scripts"
python3 tianji_runner.py --daily 2>&1 | tail -20
echo ""
echo -e "${GREEN}  ✅ 采集完成!${NC}"

# 5. 查看日报
REPORT=$(ls -t ~/tianji-data/reports/daily-*.md 2>/dev/null | head -1)
if [ -f "$REPORT" ]; then
    echo -e "${GREEN}  📄 日报已生成: $REPORT${NC}"
fi

# 6. 设置定时任务 (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo -e "${YELLOW}  ⏰ 是否设置每天 08:00 自动运行? (推荐)${NC}"
    echo "     按回车继续, 输入 n 跳过: "
    read -r choice
    if [ "$choice" != "n" ] && [ "$choice" != "N" ]; then
        PLIST="$HOME/Library/LaunchAgents/com.tianji.daily.plist"
        cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.tianji.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which python3)</string>
        <string>$REPO_DIR/scripts/tianji_runner.py</string>
        <string>--daily</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>$REPO_DIR/scripts</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
        launchctl load "$PLIST" 2>/dev/null || true
        echo -e "${GREEN}  ✅ 定时任务已配置! 每天 08:00 自动采集${NC}"
    fi
fi

# 7. 完成
echo ""
echo -e "${BLUE}  ==================================${NC}"
echo -e "${GREEN}  🎉 天玑就绪!!${NC}"
echo -e "${BLUE}  ==================================${NC}"
echo ""
echo "  手动运行:  cd ~/tianji/scripts && python3 tianji_runner.py"
echo "  查看日报:  cat ~/tianji-data/reports/daily-*.md"
echo "  配置扩展:  cd ~/tianji/scripts && python3 tianji_setup.py"
echo ""
echo -e "${BLUE}  🌐 https://github.com/lupo168/tianji${NC}"
echo ""
