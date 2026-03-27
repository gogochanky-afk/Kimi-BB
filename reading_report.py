#!/usr/bin/env python3
"""
Hugo Sammie 全家閱讀推送系統
每週日推送：成人一本書 + 孩子閱讀計劃
"""

import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')

def send_telegram(message, chat_id):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode()).get('ok', False)
    except Exception as e:
        print(f"發送失敗: {e}")
        return False

def get_weekly_books():
    """本週書單（輪換）- 實際可擴展數據庫"""
    week_num = datetime.now().isocalendar()[1]
    
    adult_books = [
        {
            "title": "《窮查理的普通常識》",
            "author": "查理·芒格",
            "theme": "多元思維模型",
            "why": "投資不只看財報，要懂心理學、物理學、歷史",
            "action": "本週檢視：是否有用單一視角做決定？"
        },
        {
            "title": "《原則》",
            "author": "雷·達里奧",
            "theme": "極度透明 + 系統化決策",
            "why": "家族辦公室需要清晰原則，不是隨性決定",
            "action": "寫下3條你的投資原則"
        },
        {
            "title": "《富過三代》",
            "author": "詹姆斯·休斯",
            "theme": "家族傳承",
            "why": "財富傳承不只是錢，是價值觀和家族文化",
            "action": "和孩子討論：我們家最重視什麼？"
        },
        {
            "title": "《刻意練習》",
            "author": "安德斯·艾瑞克森",
            "theme": "成長型思維",
            "why": "孩子教育：天賦不重要，方法才重要",
            "action": "觀察孩子練琴/練字，給予過程讚美"
        }
    ]
    
    # 根據週數輪換
    book = adult_books[week_num % len(adult_books)]
    
    return book

def get_kids_reading_plan():
    """孩子本週閱讀計劃"""
    plans = {
        "Candice (10歲)": {
            "推薦": "《哈利波特》系列 / 《神奇樹屋》",
            "主題": "勇氣與友誼",
            "活動": "讀完後畫故事地圖",
            "免費資源": "Libby App + 香港圖書館"
        },
        "Freya (8歲)": {
            "推薦": "《老鼠記者》/ 《樂高城市》",
            "主題": "冒險與創意",
            "活動": "用樂高重現故事場景",
            "免費資源": "Epic! (試用) / 圖書館"
        },
        "Rosalie (5歲)": {
            "推薦": "繪本《情緒小怪獸》/ 《好餓的毛毛蟲》",
            "主題": "情緒認識 + 成長",
            "活動": "讀完後演一遍",
            "免費資源": "YouTube Storytime / 圖書館"
        },
        "Zane (2歲+)": {
            "推薦": "觸摸書《Pat the Bunny》/ 認知圖卡",
            "主題": "感官探索",
            "活動": "指認顏色 + 數數",
            "免費資源": "圖書館借閱"
        }
    }
    return plans

def generate_reading_report():
    """生成閱讀報告"""
    book = get_weekly_books()
    kids_plan = get_kids_reading_plan()
    
    lines = []
    lines.append("📚 <b>Hugo Sammie 全家閱讀計劃</b>")
    lines.append(f"📅 {datetime.now().strftime('%m月%d日')} 本週推薦")
    lines.append("")
    
    # 成人書籍
    lines.append("<b>📖 【本週精讀】</b>")
    lines.append(f"書名：{book['title']}")
    lines.append(f"作者：{book['author']}")
    lines.append(f"主題：{book['theme']}")
    lines.append("")
    lines.append(f"💡 <b>為什麼讀這本：</b>")
    lines.append(book['why'])
    lines.append("")
    lines.append(f"🎯 <b>本週實踐：</b>")
    lines.append(book['action'])
    lines.append("")
    
    # 孩子閱讀
    lines.append("<b>👧👦 【孩子本週閱讀】</b>")
    for name, plan in kids_plan.items():
        lines.append(f"\n{name}:")
        lines.append(f"📖 {plan['推薦']}")
        lines.append(f"🎯 主題：{plan['主題']}")
        lines.append(f"🎨 活動：{plan['活動']}")
        lines.append(f"💰 資源：{plan['免費資源']}")
    
    lines.append("")
    lines.append("<b>💡 【付費資源建議】</b>")
    lines.append("• Epic! ($8/月) - 4萬本兒童互動書，4孩共用")
    lines.append("• 得到 ($10/月) - 每天一本書精華，省時間")
    lines.append("• 兩者合計 ~$220/年 = 全家知識投資")
    lines.append("")
    
    lines.append("<i>📌 小GoGo 建議：先試用 Epic! 免費版，孩子喜歡再訂閱</i>")
    
    return "\n".join(lines)

def main():
    report = generate_reading_report()
    send_telegram(report, CHAT_ID)
    send_telegram(report, GROUP_ID)
    print("閱讀計劃推送完成")

if __name__ == "__main__":
    main()
