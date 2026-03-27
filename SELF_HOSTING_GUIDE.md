# Hugo Sammie 家族辦公室 - OpenClaw 自建伺服器指南

完整的一鍵部署腳本和 Docker 配置，建立你的私人 AI 辦公室。

## 🚀 快速開始（3選1）

### 方法一：一鍵腳本（推薦新手）

```bash
# 1. 下載腳本
curl -O https://raw.githubusercontent.com/gogochanky-afk/Kimi-BB/main/deploy_openclaw.sh

# 2. 給予執行權限
chmod +x deploy_openclaw.sh

# 3. 運行（需要 root）
sudo ./deploy_openclaw.sh

# 4. 配置 API Keys
sudo nano /etc/openclaw/config.json

# 5. 啟動服務
sudo systemctl start openclaw-gateway
sudo systemctl start openclaw-agent
```

### 方法二：Docker Compose（推薦）

```bash
# 1. 克隆倉庫
git clone https://github.com/gogochanky-afk/Kimi-BB.git
 cd Kimi-BB

# 2. 配置環境變量
cp .env.example .env
nano .env  # 填入你的 API Keys

# 3. 啟動
 docker-compose up -d

# 4. 檢查狀態
 curl http://localhost:3000/status
```

### 方法三：手動安裝（專家用戶）

見下方「詳細手動安裝」章節。

---

## 📋 前置要求

### 系統要求
- **OS**: Ubuntu 22.04+ / Debian 12+ / CentOS 9+
- **CPU**: 2 核+
- **RAM**: 4GB+
- **Storage**: 20GB+
- **Network**: 可訪問外網（連接 AI API）

### 必備 API Keys

| 服務 | 用途 | 獲取方式 |
|------|------|---------|
| **Kimi API** | AI 對話 | https://platform.moonshot.cn |
| **Telegram Bot** | 消息推送 | @BotFather |

### 可選 API Keys

| 服務 | 用途 |
|------|------|
| Notion | 知識庫 |
| Google Calendar | 日程同步 |
| GitHub | 自動化腳本 |
| Alpha Vantage | 股票數據 |

---

## 🔧 詳細配置

### 1. Kimi API 設置

```bash
# 註冊 https://platform.moonshot.cn
# 創建 API Key
# 複製到 config.json 或 .env
```

### 2. Telegram Bot 設置

```bash
# 1. 找 @BotFather
# 2. /newbot
# 3. 取名（如 hugosammie_office_bot）
# 4. 複製 Token（如 1234567890:ABC...）
# 5. 把 Bot 加入你的群組
# 6. 發一條消息啟動對話
```

### 3. Notion 設置（可選）

```bash
# 1. https://www.notion.so/my-integrations
# 2. 創建 Integration
# 3. 複製 Internal Integration Token
# 4. 分享資料庫給 Integration
```

---

## 📁 目錄結構

```
/opt/openclaw/           # 安裝目錄
├── gateway/            # Gateway 服務
├── agent/              # Python Agent
└── skills/             # 技能插件

/etc/openclaw/          # 配置目錄
├── config.json         # 主配置
└── .env               # 環境變量

/var/lib/openclaw/      # 數據目錄
├── workspace/          # 工作區
├── memory/             # 記憶文件
└── logs/               # 日誌
```

---

## 🎮 常用命令

### 系統服務管理

```bash
# 查看狀態
sudo systemctl status openclaw-gateway
sudo systemctl status openclaw-agent

# 啟動/停止/重啟
sudo systemctl start openclaw-gateway
sudo systemctl stop openclaw-gateway
sudo systemctl restart openclaw-gateway

# 查看日誌
sudo journalctl -u openclaw-gateway -f
sudo journalctl -u openclaw-agent -f

# 設置開機自啟
sudo systemctl enable openclaw-gateway
sudo systemctl enable openclaw-agent
```

### Docker 管理

```bash
# 查看狀態
docker-compose ps
docker-compose logs -f

# 重啟服務
docker-compose restart
docker-compose down && docker-compose up -d

# 更新鏡像
docker-compose pull
docker-compose up -d
```

---

## 🔒 安全配置

### 1. 防火牆設置

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 3000/tcp # OpenClaw (僅限內網)
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 2. Nginx + SSL (Let's Encrypt)

```bash
# 安裝 certbot
sudo apt install certbot python3-certbot-nginx

# 申請證書
sudo certbot --nginx -d your-domain.com

# 自動續期測試
sudo certbot renew --dry-run
```

### 3. Fail2ban 防暴力破解

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 🐛 故障排除

### 問題：服務無法啟動

```bash
# 檢查日誌
sudo journalctl -u openclaw-gateway --no-pager -n 50

# 檢查配置語法
sudo cat /etc/openclaw/config.json | jq .

# 檢查端口占用
sudo netstat -tlnp | grep 3000
```

### 問題：API 無法連接

```bash
# 測試 Kimi API
curl https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer your-api-key"

# 測試本地 Gateway
curl http://localhost:3000/status
```

### 問題：Telegram 收不到消息

```bash
# 測試 Bot Token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe

# 測試發送消息
curl -X POST https://api.telegram.org/bot<TOKEN>/sendMessage \
  -d chat_id=<CHAT_ID> \
  -d text="測試消息"
```

---

## 📊 監控與維護

### 日誌輪替

```bash
# 安裝 logrotate
sudo apt install logrotate

# 配置
sudo nano /etc/logrotate.d/openclaw
```

### 備份腳本

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
tar -czf "/backup/openclaw-$DATE.tar.gz" \
  /etc/openclaw \
  /var/lib/openclaw
```

### 資源監控

```bash
# 安裝 htop
sudo apt install htop

# 查看實時資源使用
htop
```

---

## 🔄 更新升級

### 更新 Gateway

```bash
cd /opt/openclaw/gateway
git pull
npm install
npm run build
sudo systemctl restart openclaw-gateway
```

### 更新 Agent

```bash
cd /opt/openclaw/agent
source venv/bin/activate
pip install --upgrade openclaw-agent
sudo systemctl restart openclaw-agent
```

---

## 📝 自定義技能開發

```python
# /opt/openclaw/skills/my-skill/SKILL.md
# 技能定義文件

# /opt/openclaw/skills/my-skill/main.py
# 技能執行腳本
```

見 `skills/` 目錄範例。

---

## 💡 最佳實踐

1. **定期備份** - 設置每日自動備份 `config/` 和 `data/`
2. **監控告警** - 使用 UptimeRobot 監控服務狀態
3. **日誌審計** - 定期檢查日誌，發現異常及時處理
4. **安全更新** - 每月更新系統和依賴包
5. **測試環境** - 重要更新先在測試環境驗證

---

## 📞 支援

- **GitHub Issues**: https://github.com/gogochanky-afk/Kimi-BB/issues
- **OpenClaw Docs**: https://docs.openclaw.ai
- **社群**: https://discord.gg/clawd

---

**Hugo Sammie 家族辦公室 - 自主可控的 AI 基礎設施** 🏛️
