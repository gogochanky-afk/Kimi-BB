# A+C 組合方案部署指南

## 方案 A: 立即生效（今天就能用）

### 步驟
1. 打開 Google Apps Script: https://script.google.com
2. 進入您的專案
3. 刪除所有舊代碼
4. 複製貼上: https://raw.githubusercontent.com/gogochanky-afk/Kimi-BB/main/appscript_v2_ac.js
5. 保存 (Ctrl+S)
6. 點擊 "運行" → 選擇 "test" → 授權 → 測試

### 效果
- Telegram: 照常收到通知
- OpenClaw: 同時收到通知（暫時用 httpbin.org 測試）
- 明天開始自動運行

---

## 方案 C: Hetzner 專業版（等 Hetzner 有空時部署）

### 步驟
1. SSH 進 Hetzner
2. 運行:
   ```bash
   curl -O https://raw.githubusercontent.com/gogochanky-afk/Kimi-BB/main/deploy_hetzner_webhook.sh
   chmod +x deploy_hetzner_webhook.sh
   ./deploy_hetzner_webhook.sh
   ```
3. 記下顯示的 IP:port
4. 更新 Google Apps Script 中的 webhook URL
5. 完成！

### 效果
- 完整的 Webhook 接收器
- 可擴展（連接真實股票 API）
- 專屬於您的基礎設施
