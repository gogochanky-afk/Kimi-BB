#!/bin/bash
# =============================================================================
# Hugo Sammie 家族辦公室 - OpenClaw 自建伺服器部署腳本
# 一鍵部署完整指南
# 適用：Ubuntu 22.04+ / Debian 12+ / CentOS 9+
# =============================================================================

set -e  # 遇到錯誤立即停止

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置變量
INSTALL_DIR="/opt/openclaw"
CONFIG_DIR="/etc/openclaw"
DATA_DIR="/var/lib/openclaw"
LOG_DIR="/var/log/openclaw"
SERVICE_USER="openclaw"

# 版本
GATEWAY_VERSION="2026.2.13"
AGENT_VERSION="1.0.0"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Hugo Sammie 家族辦公室 - OpenClaw 伺服器部署腳本          ║"
echo "║     完整自動化安裝 (Ubuntu/Debian/CentOS)                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# =============================================================================
# 步驟 1: 系統檢查
# =============================================================================
echo -e "\n${YELLOW}[1/8] 系統檢查...${NC}"

# 檢查是否 root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}請使用 sudo 或 root 權限運行此腳本${NC}"
    exit 1
fi

# 檢測操作系統
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
    echo -e "${GREEN}檢測到系統: $NAME $VERSION${NC}"
else
    echo -e "${RED}無法檢測操作系統${NC}"
    exit 1
fi

# 檢查架構
ARCH=$(uname -m)
if [ "$ARCH" != "x86_64" ] && [ "$ARCH" != "aarch64" ]; then
    echo -e "${RED}不支持的架構: $ARCH (需要 x86_64 或 aarch64)${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 系統檢查通過${NC}"

# =============================================================================
# 步驟 2: 安裝依賴
# =============================================================================
echo -e "\n${YELLOW}[2/8] 安裝系統依賴...${NC}"

install_deps() {
    case $OS in
        ubuntu|debian)
            apt-get update
            apt-get install -y \
                curl wget git jq \
                nodejs npm \
                python3 python3-pip python3-venv \
                docker.io docker-compose \
                nginx certbot python3-certbot-nginx \
                ufw fail2ban \
                htop tree vim
            ;;
        centos|rhel|fedora|rocky|almalinux)
            yum update -y
            yum install -y \
                curl wget git jq \
                nodejs npm \
                python3 python3-pip \
                docker docker-compose \
                nginx certbot python3-certbot-nginx \
                firewalld fail2ban \
                htop tree vim
            systemctl enable firewalld
            systemctl start firewalld
            ;;
        *)
            echo -e "${RED}不支持的操作系統: $OS${NC}"
            exit 1
            ;;
    esac
}

install_deps
echo -e "${GREEN}✓ 依賴安裝完成${NC}"

# =============================================================================
# 步驟 3: 創建用戶和目錄
# =============================================================================
echo -e "\n${YELLOW}[3/8] 創建服務用戶和目錄...${NC}"

# 創建服務用戶
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$DATA_DIR" -M "$SERVICE_USER"
    usermod -aG docker "$SERVICE_USER"
    echo -e "${GREEN}創建用戶: $SERVICE_USER${NC}"
fi

# 創建目錄
mkdir -p "$INSTALL_DIR"/{gateway,agent,skills}
mkdir -p "$CONFIG_DIR"
mkdir -p "$DATA_DIR"/{memory,workspace,logs}
mkdir -p "$LOG_DIR"

# 設置權限
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" "$DATA_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"

echo -e "${GREEN}✓ 目錄結構創建完成${NC}"

# =============================================================================
# 步驟 4: 安裝 Gateway
# =============================================================================
echo -e "\n${YELLOW}[4/8] 安裝 OpenClaw Gateway...${NC}"

cd "$INSTALL_DIR/gateway"

# 下載 Gateway
curl -L "https://github.com/openclaw/openclaw/releases/download/v${GATEWAY_VERSION}/openclaw-gateway-linux-${ARCH}.tar.gz" \
    -o gateway.tar.gz

tar -xzf gateway.tar.gz
rm gateway.tar.gz

# 安裝 Node 依賴
npm install --production

echo -e "${GREEN}✓ Gateway 安裝完成${NC}"

# =============================================================================
# 步驟 5: 安裝 Python Agent
# =============================================================================
echo -e "\n${YELLOW}[5/8] 安裝 Python Agent...${NC}"

cd "$INSTALL_DIR/agent"

# 創建虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install --upgrade pip
pip install \
    openclaw-agent \
    requests \
    pyyaml \
    python-telegram-bot \
    yfinance \
    pandas \
    notion-client \
    google-api-python-client

# 安裝 Skills
mkdir -p "$INSTALL_DIR/skills"
cd "$INSTALL_DIR/skills"

# 下載常用 Skills
SKILLS_REPO="https://github.com/openclaw/skills"
git clone --depth 1 "$SKILLS_REPO" . 2>/dev/null || true

echo -e "${GREEN}✓ Agent 和 Skills 安裝完成${NC}"

# =============================================================================
# 步驟 6: 生成配置文件
# =============================================================================
echo -e "\n${YELLOW}[6/8] 生成配置文件...${NC}"

# 生成隨機密鑰
GATEWAY_SECRET=$(openssl rand -hex 32)
SESSION_KEY=$(openssl rand -hex 32)

cat > "$CONFIG_DIR/config.json" << EOF
{
  "gateway": {
    "version": "${GATEWAY_VERSION}",
    "port": 3000,
    "host": "0.0.0.0",
    "secret": "${GATEWAY_SECRET}",
    "sessionKey": "${SESSION_KEY}",
    "logLevel": "info",
    "logDir": "${LOG_DIR}"
  },
  "models": {
    "default": {
      "provider": "kimi",
      "model": "kimi-coding/k2p5",
      "apiKey": "YOUR_KIMI_API_KEY_HERE",
      "baseUrl": "https://api.moonshot.cn/v1",
      "timeoutMs": 120000,
      "maxRetries": 3
    },
    "fallback": {
      "provider": "openai",
      "model": "gpt-4o",
      "apiKey": "YOUR_OPENAI_API_KEY_HERE"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN",
      "webhookUrl": "https://your-domain.com/webhook/telegram",
      "allowedChatIds": [],
      "adminChatId": null
    },
    "kimi-claw": {
      "enabled": true
    },
    "discord": {
      "enabled": false,
      "token": "YOUR_DISCORD_BOT_TOKEN"
    }
  },
  "agents": {
    "main": {
      "type": "python",
      "path": "${INSTALL_DIR}/agent",
      "venv": "${INSTALL_DIR}/agent/venv",
      "env": {
        "WORKSPACE": "${DATA_DIR}/workspace",
        "MEMORY_DIR": "${DATA_DIR}/memory",
        "LOG_LEVEL": "info"
      }
    }
  },
  "skills": {
    "path": "${INSTALL_DIR}/skills",
    "autoLoad": true,
    "enabled": [
      "memory-manager",
      "stock-monitor",
      "weather",
      "web-search"
    ]
  },
  "memory": {
    "type": "file",
    "path": "${DATA_DIR}/memory",
    "autoBackup": true,
    "backupInterval": "24h"
  },
  "security": {
    "enableAuth": true,
    "allowedIPs": [],
    "rateLimit": {
      "enabled": true,
      "requestsPerMinute": 60
    }
  },
  "cron": {
    "enabled": true,
    "jobsDir": "${CONFIG_DIR}/cron"
  }
}
EOF

# 創建環境變量文件
cat > "$CONFIG_DIR/.env" << EOF
# OpenClaw 環境變量
GATEWAY_SECRET=${GATEWAY_SECRET}
SESSION_KEY=${SESSION_KEY}
WORKSPACE=${DATA_DIR}/workspace
MEMORY_DIR=${DATA_DIR}/memory
LOG_DIR=${LOG_DIR}

# API Keys (請填入你的密鑰)
KIMI_API_KEY=your_kimi_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
NOTION_TOKEN=your_notion_token_here

# 其他配置
TZ=Asia/Shanghai
LANG=zh_TW.UTF-8
EOF

chmod 600 "$CONFIG_DIR/.env"

echo -e "${GREEN}✓ 配置文件生成完成${NC}"
echo -e "${YELLOW}⚠ 請編輯 ${CONFIG_DIR}/config.json 填入你的 API Keys${NC}"

# =============================================================================
# 步驟 7: 創建系統服務
# =============================================================================
echo -e "\n${YELLOW}[7/8] 創建系統服務...${NC}"

# Gateway 服務
cat > /etc/systemd/system/openclaw-gateway.service << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target docker.service

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR/gateway
ExecStart=/usr/bin/node $INSTALL_DIR/gateway/dist/index.js
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
Environment=NODE_ENV=production
EnvironmentFile=$CONFIG_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

# Agent 服務
cat > /etc/systemd/system/openclaw-agent.service << EOF
[Unit]
Description=OpenClaw Python Agent
After=openclaw-gateway.service

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR/agent
ExecStart=$INSTALL_DIR/agent/venv/bin/python -m openclaw.agent
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=$CONFIG_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

# 重新載入 systemd
systemctl daemon-reload

echo -e "${GREEN}✓ 系統服務創建完成${NC}"

# =============================================================================
# 步驟 8: 防火牆和 SSL
# =============================================================================
echo -e "\n${YELLOW}[8/8] 配置防火牆和 SSL...${NC}"

# 配置防火牆
case $OS in
    ubuntu|debian)
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow 22/tcp    # SSH
        ufw allow 80/tcp    # HTTP
        ufw allow 443/tcp   # HTTPS
        ufw allow 3000/tcp  # OpenClaw Gateway
        ufw --force enable
        ;;
    centos|rhel|fedora)
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --add-port=3000/tcp
        firewall-cmd --reload
        ;;
esac

echo -e "${GREEN}✓ 防火牆配置完成${NC}"

# =============================================================================
# 完成！
# =============================================================================
echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════╗"
echo "║                     🎉 部署完成！                              ║"
echo "╚════════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${BLUE}安裝路徑:${NC}"
echo "  Gateway:  $INSTALL_DIR/gateway"
echo "  Agent:    $INSTALL_DIR/agent"
echo "  Skills:   $INSTALL_DIR/skills"
echo "  Config:   $CONFIG_DIR"
echo "  Data:     $DATA_DIR"
echo "  Logs:     $LOG_DIR"

echo -e "\n${BLUE}下一步:${NC}"
echo "  1. 編輯配置文件:"
echo "     sudo nano $CONFIG_DIR/config.json"
echo ""
echo "  2. 填入你的 API Keys:"
echo "     - Kimi API Key (sk-...)"
echo "     - Telegram Bot Token"
echo "     - 其他需要的密鑰"
echo ""
echo "  3. 啟動服務:"
echo "     sudo systemctl start openclaw-gateway"
echo "     sudo systemctl start openclaw-agent"
echo ""
echo "  4. 設置開機自啟:"
echo "     sudo systemctl enable openclaw-gateway"
echo "     sudo systemctl enable openclaw-agent"
echo ""
echo "  5. 檢查狀態:"
echo "     sudo systemctl status openclaw-gateway"
echo "     curl http://localhost:3000/status"

echo -e "\n${BLUE}常用命令:${NC}"
echo "  查看日誌:   sudo journalctl -u openclaw-gateway -f"
echo "  重啟服務:   sudo systemctl restart openclaw-gateway"
echo "  停止服務:   sudo systemctl stop openclaw-gateway"

echo -e "\n${YELLOW}⚠ 安全提醒:${NC}"
echo "  • 請務必修改默認密鑰"
echo "  • 建議使用 Nginx + SSL (Let's Encrypt)"
echo "  • 定期備份 $DATA_DIR 目錄"
echo "  • 配置 fail2ban 防止暴力破解"

echo -e "\n${GREEN}Hugo Sammie 家族辦公室 - 系統就緒！${NC}"
