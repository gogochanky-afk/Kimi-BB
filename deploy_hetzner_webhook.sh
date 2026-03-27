#!/bin/bash
# =============================================================================
# Hugo Sammie 家族辦公室 - Hetzner 專業版 Webhook 接收器
# 方案 C: 完整自動化，接收 Google Apps Script 通知並轉發給 OpenClaw
# =============================================================================

set -e

echo "🚀 Hugo Sammie 家族辦公室 - Hetzner Webhook 部署腳本"
echo "========================================================"

# 配置
INSTALL_DIR="$HOME/hugo-office-webhook"
SERVICE_NAME="hugo-webhook"
PORT="3001"

# 檢查是否已有運行實例
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 $PORT 已被占用，可能已經部署過"
    echo "如果需要重新部署，請先停止現有服務"
    exit 1
fi

echo ""
echo "📁 步驟 1: 創建目錄..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo ""
echo "📝 步驟 2: 創建 Webhook 接收器..."

cat > webhook_server.py << 'PYEOF'
#!/usr/bin/env python3
"""
Hugo Sammie 家族辦公室 Webhook 接收器
接收 Google Apps Script 通知，轉發給 OpenClaw
"""

import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os

# 配置
OPENCLAW_WEBHOOK_URL = os.getenv('OPENCLAW_WEBHOOK_URL', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def log_message(msg):
    """記錄日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")

def forward_to_openclaw(data):
    """轉發給 OpenClaw"""
    if not OPENCLAW_WEBHOOK_URL:
        log_message("⚠️  未配置 OPENCLAW_WEBHOOK_URL")
        return False
    
    try:
        req = urllib.request.Request(
            OPENCLAW_WEBHOOK_URL,
            data=json.dumps(data).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            log_message(f"✅ 已轉發給 OpenClaw: {response.status}")
            return True
    except Exception as e:
        log_message(f"❌ 轉發失敗: {e}")
        return False

def send_telegram(message):
    """發送 Telegram 消息"""
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }).encode()
        urllib.request.urlopen(url, data=data, timeout=30)
    except Exception as e:
        log_message(f"Telegram 發送失敗: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """處理 POST 請求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            # 記錄接收
            source = data.get('source', 'unknown')
            msg_type = data.get('type', 'general')
            log_message(f"📨 收到通知: {source} / {msg_type}")
            
            # 轉發給 OpenClaw
            forward_to_openclaw(data)
            
            # 返回成功
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        except Exception as e:
            log_message(f"❌ 處理請求失敗: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_GET(self):
        """健康檢查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'running',
            'service': 'Hugo Sammie Office Webhook'
        }).encode())
    
    def log_message(self, format, *args):
        """禁用默認日志"""
        pass

def main():
    port = int(os.getenv('PORT', 3001))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    log_message(f"🚀 Webhook 服務啟動於端口 {port}")
    log_message(f"📡 等待 Google Apps Script 通知...")
    server.serve_forever()

if __name__ == '__main__':
    main()
PYEOF

chmod +x webhook_server.py

echo ""
echo "⚙️  步驟 3: 創建環境變量配置..."
cat > .env << 'EOF'
# Webhook 服務配置
PORT=3001

# Telegram（用於備份通知）
TELEGRAM_BOT_TOKEN=8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc
TELEGRAM_CHAT_ID=7042296651

# OpenClaw 接收地址（需要配置您的 OpenClaw webhook URL）
# OPENCLAW_WEBHOOK_URL=https://your-openclaw-instance.com/webhook/hugo-office
EOF

echo ""
echo "📝 步驟 4: 創建 systemd 服務..."

cat > /tmp/hugo-webhook.service << EOF
[Unit]
Description=Hugo Sammie Office Webhook Receiver
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=/usr/bin/python3 $INSTALL_DIR/webhook_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/hugo-webhook.service /etc/systemd/system/
sudo systemctl daemon-reload

echo ""
echo "🔥 步驟 5: 開放防火牆..."
sudo ufw allow 3001/tcp 2>/dev/null || true
sudo firewall-cmd --permanent --add-port=3001/tcp 2>/dev/null || true
sudo firewall-cmd --reload 2>/dev/null || true

echo ""
echo "🚀 步驟 6: 啟動服務..."
sudo systemctl enable hugo-webhook
sudo systemctl start hugo-webhook
sleep 2

# 檢查狀態
if systemctl is-active --quiet hugo-webhook; then
    echo "✅ 服務已成功啟動！"
    IP=$(curl -s ifconfig.me || echo "YOUR_SERVER_IP")
    echo ""
    echo "📡 Webhook URL: http://$IP:3001"
    echo "📝 健康檢查: http://$IP:3001 (用瀏覽器訪問測試)"
else
    echo "❌ 服務啟動失敗，查看日誌: sudo journalctl -u hugo-webhook -n 50"
fi

echo ""
echo "========================================================"
echo "✅ Hetzner Webhook 部署完成！"
echo "========================================================"
echo ""
echo "📂 安裝位置: $INSTALL_DIR"
echo "📜 服務名稱: hugo-webhook"
echo "🔌 端口: 3001"
echo ""
echo "🔧 常用命令:"
echo "  查看狀態: sudo systemctl status hugo-webhook"
echo "  查看日誌: sudo journalctl -u hugo-webhook -f"
echo "  重啟服務: sudo systemctl restart hugo-webhook"
echo ""
echo "📝 下一步:"
echo "  1. 記下您的服務器 IP 地址"
echo "  2. 在 .env 文件中配置 OPENCLAW_WEBHOOK_URL"
echo "  3. 更新 Google Apps Script 中的 webhook URL"
echo "  4. 測試連接！"
