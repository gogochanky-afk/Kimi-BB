# Hugo Sammie 家族辦公室 - Vercel 部署版

## 🚀 一鍵部署到 Vercel

### 步驟 1：點擊部署
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/gogochanky-afk/Kimi-BB)

### 步驟 2：配置環境變量
在 Vercel 設置中添加：

```
TELEGRAM_BOT_TOKEN=8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc
TELEGRAM_CHAT_ID=7042296651
TELEGRAM_GROUP_ID=-5153249366
```

### 步驟 3：完成！
Vercel 會自動：
- ✅ 部署 API 端點
- ✅ 設置 Cron 定時任務
- ✅ 每天自動推送

---

## ⏰ 定時任務

| 時間 | 端點 | 內容 |
|------|------|------|
| 7:45 AM | `/api/schedule_report` | 家庭日程 |
| 9:00 AM | `/api/news_report` | 全球晨報 |
| 8:30 PM | `/api/premarket_report` | 美股盤前 (週一到五) |
| 10:30 PM | `/api/opportunity_check` | 機會檢查 (週一到五) |
| 週日 10:00 AM | `/api/reading_report` | 閱讀計劃 |

---

## 📂 文件結構

```
api/
├── schedule_report.py    # 家庭日程
├── news_report.py        # 全球晨報
├── premarket_report.py   # 美股盤前
├── opportunity_check.py  # 機會檢查
└── reading_report.py     # 閱讀計劃
vercel.json               # Vercel 配置
```

---

## 🔧 手動測試

部署後可以手動訪問測試：
```
https://your-project.vercel.app/api/schedule_report
```

---

**完全托管，零維護，免費使用！** 🎉
