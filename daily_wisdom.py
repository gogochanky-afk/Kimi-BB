#!/usr/bin/env python3
"""
Hugo Sammie 個人每日智識推送
每天 8:00 AM 推送一本實用書籍的核心精華
"""

import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GROUP_ID = os.getenv('TELEGRAM_GROUP_ID', '-5153249366')

# 100本實用書籍知識庫（精簡版 - 零成本）
BOOKS = [
    {
        "title": "原子習慣",
        "author": "James Clear",
        "category": "效率",
        "core": "每天進步1%，一年後會進步37倍。關鍵不在目標，而在系統。",
        "action": "今天開始：把想做的事縮小到2分鐘就能完成。",
        "quote": "You do not rise to the level of your goals. You fall to the level of your systems."
    },
    {
        "title": "原則",
        "author": "Ray Dalio",
        "category": "投資",
        "core": "極度求真 + 極度透明 = 最佳決策。失敗是進化的過程。",
        "action": "記錄今天一個錯誤，寫下教訓。",
        "quote": "Pain + Reflection = Progress"
    },
    {
        "title": "窮查理的普通常識",
        "author": "Charlie Munger",
        "category": "投資",
        "core": "多元思維模型。反過來想，總是反過來想。",
        "action": "今天做決定前，問自己：什麼會讓這件事失敗？",
        "quote": "Invert, always invert."
    },
    {
        "title": "從0到1",
        "author": "Peter Thiel",
        "category": "創業",
        "core": "競爭是給失敗者的。壟斷才是商業的終點。",
        "action": "思考：你的事業有什麼是別人複製不了的？",
        "quote": "Competition is for losers."
    },
    {
        "title": "人類大歷史",
        "author": "Yuval Noah Harari",
        "category": "認知",
        "core": "人類勝出因為會講故事。認知革命 > 基因演化。",
        "action": "觀察今天聽到的故事，思考背後的敘事邏輯。",
        "quote": "Humans control the world because we are the only animals that can cooperate flexibly in large numbers."
    }
]

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

def get_today_book():
    """根據日期循環選擇書籍"""
    day_of_year = datetime.now().timetuple().tm_yday
    return BOOKS[day_of_year % len(BOOKS)]

def main():
    book = get_today_book()
    
    lines = []
    lines.append(f"📚 <b>每日智識 | {book['category']}</b>")
    lines.append(f"《{book['title']}》by {book['author']}")
    lines.append("")
    lines.append(f"💡 <b>核心觀點：</b>")
    lines.append(book['core'])
    lines.append("")
    lines.append(f"🎯 <b>今日行動：</b>")
    lines.append(book['action'])
    lines.append("")
    lines.append(f"📖 <i>{book['quote']}</i>")
    lines.append("")
    lines.append("— 來自 Hugo Sammie 家族辦公室")
    
    report = "\n".join(lines)
    
    # 推送到私人
    send_telegram(report, CHAT_ID)
    print(f"已推送到私人: {CHAT_ID}")
    
    # 推送到群組
    send_telegram(report, GROUP_ID)
    print(f"已推送到群組: {GROUP_ID}")

if __name__ == "__main__":
    main()
