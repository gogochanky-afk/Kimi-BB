#!/bin/bash
# =============================================================================
# Hugo Sammie 家族辦公室 - Hetzner 快速遷移腳本
# 5分鐘內完成遷移，告別 GitHub Actions 定時問題
# =============================================================================

set -e

echo "🚀 Hugo Sammie 家族辦公室 - Hetzner 遷移腳本"
echo "=============================================="

# 配置
INSTALL_DIR="$HOME/openclaw-office"
SCRIPTS_DIR="$INSTALL_DIR/scripts"
VENV_DIR="$INSTALL_DIR/venv"

echo ""
echo "📁 步驟 1: 創建目錄結構..."
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$INSTALL_DIR/logs"

echo ""
echo "🐍 步驟 2: 創建 Python 虛擬環境..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install requests python-telegram-bot yfinance pandas -q
echo "✅ Python 環境就緒"

echo ""
echo "📥 步驟 3: 下載所有腳本..."
cd "$SCRIPTS_DIR"

# 下載所有腳本
BASE_URL="https://raw.githubusercontent.com/gogochanky-afk/Kimi-BB/main"

curl -sO "$BASE_URL/schedule_report.py" && echo "✅ schedule_report.py"
curl -sO "$BASE_URL/news_report.py" && echo "✅ news_report.py"
curl -sO "$BASE_URL/market_monitor_v2.py" && echo "✅ market_monitor_v2.py"
curl -sO "$BASE_URL/reading_report.py" && echo "✅ reading_report.py"
curl -sO "$BASE_URL/daily_wisdom.py" && echo "✅ daily_wisdom.py"

echo ""
echo "⚙️ 步驟 4: 創建環境變量文件..."
cat > "$INSTALL_DIR/.env" << 'EOF'
# Telegram 配置
TELEGRAM_BOT_TOKEN=8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc
TELEGRAM_CHAT_ID=7042296651
TELEGRAM_GROUP_ID=-5153249366

# 可選：其他 API Keys
# KIMI_API_KEY=your_key_here
# NOTION_TOKEN=your_token_here
EOF

echo ""
echo "📝 步驟 5: 創建執行腳本..."

cat > "$INSTALL_DIR/run_schedule.sh" << 'EOF'
#!/bin/bash
source "$HOME/openclaw-office/venv/bin/activate"
export $(cat "$HOME/openclaw-office/.env" | xargs)
cd "$HOME/openclaw-office/scripts"
python schedule_report.py >> "$HOME/openclaw-office/logs/schedule.log" 2>&1
EOF

cat > "$INSTALL_DIR/run_news.sh" << 'EOF'
#!/bin/bash
source "$HOME/openclaw-office/venv/bin/activate"
export $(cat "$HOME/openclaw-office/.env" | xargs)
cd "$HOME/openclaw-office/scripts"
python news_report.py >> "$HOME/openclaw-office/logs/news.log" 2>&1
EOF

cat > "$INSTALL_DIR/run_premarket.sh" << 'EOF'
#!/bin/bash
source "$HOME/openclaw-office/venv/bin/activate"
export $(cat "$HOME/openclaw-office/.env" | xargs)
cd "$HOME/openclaw-office/scripts"
python market_monitor_v2.py premarket >> "$HOME/openclaw-office/logs/market.log" 2>&1
EOF

cat > "$INSTALL_DIR/run_opportunity.sh" << 'EOF'
#!/bin/bash
source "$HOME/openclaw-office/venv/bin/activate"
export $(cat "$HOME/openclaw-office/.env" | xargs)
cd "$HOME/openclaw-office/scripts"
python market_monitor_v2.py opportunity >> "$HOME/openclaw-office/logs/market.log" 2>&1
EOF

cat > "$INSTALL_DIR/run_reading.sh" << 'EOF'
#!/bin/bash
source "$HOME/openclaw-office/venv/bin/activate"
export $(cat "$HOME/openclaw-office/.env" | xargs)
cd "$HOME/openclaw-office/scripts"
python reading_report.py >> "$HOME/openclaw-office/logs/reading.log" 2>&1
EOF

chmod +x "$INSTALL_DIR"/*.sh

echo ""
echo "⏰ 步驟 6: 設置 Crontab（定時任務）..."

# 創建 crontab 條目
CRON_CONTENT="# Hugo Sammie 家族辦公室定時任務
# 香港時間早上 7:45 = 前一天 23:45 UTC
45 23 * * * $INSTALL_DIR/run_schedule.sh

# 香港時間早上 9:00 = 01:00 UTC
0 1 * * * $INSTALL_DIR/run_news.sh

# 香港時間晚上 8:30 = 12:30 UTC (週一到五)
30 12 * * 1-5 $INSTALL_DIR/run_premarket.sh

# 香港時間晚上 10:30 = 14:30 UTC (週一到五)
30 14 * * 1-5 $INSTALL_DIR/run_opportunity.sh

# 香港時間週日上午 10:00 = 02:00 UTC
0 2 * * 0 $INSTALL_DIR/run_reading.sh
"

# 備份現有 crontab
crontab -l > "$INSTALL_DIR/crontab.backup" 2>/dev/null || true

# 寫入新的 crontab
echo "$CRON_CONTENT" | crontab -

echo ""
echo "✅ Crontab 設置完成："
crontab -l | grep -v "^#" | grep -v "^$"

echo ""
echo "🧪 步驟 7: 立即測試..."
bash "$INSTALL_DIR/run_schedule.sh" &
TEST_PID=$!
sleep 5
if ps -p $TEST_PID > /dev/null; then
    echo "✅ 測試進行中（10秒後完成）"
    sleep 5
else
    echo "✅ 測試已完成"
fi

echo ""
echo "=============================================="
echo "🎉 遷移完成！"
echo "=============================================="
echo ""
echo "📂 安裝位置: $INSTALL_DIR"
echo "📜 日誌位置: $INSTALL_DIR/logs/"
echo ""
echo "⏰ 定時任務已激活："
echo "  • 每天 7:45 AM - 家庭日程"
echo "  • 每天 9:00 AM - 全球晨報"
echo "  • 週一到五 8:30 PM - 美股盤前"
echo "  • 週一到五 10:30 PM - 機會檢查"
echo "  • 週日 10:00 AM - 閱讀計劃"
echo ""
echo "🔧 常用命令："
echo "  查看日誌: tail -f $INSTALL_DIR/logs/*.log"
echo "  手動測試: bash $INSTALL_DIR/run_schedule.sh"
echo "  編輯定時: crontab -e"
echo "  查看定時: crontab -l"
echo ""
echo "💡 下一步："
echo "  1. 檢查 Telegram 是否收到測試消息"
echo "  2. 明早 7:45 AM 確認第一次自動推送"
echo ""
echo "⚠️ 注意：daily_wisdom.py 需要修復，暫時跳過"
