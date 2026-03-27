#!/usr/bin/env python3
"""
Hugo Sammie 家族日程自動推送
每天早上 8:00 發送當日行程
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

def get_schedule():
    weekday = datetime.now().weekday()  # 0=Monday
    schedules = {
        0: "📅 星期一\n• 女兒校隊至 5:00 PM\n• 中國樂器 6:45-8:00 PM\n• 🔔 提醒：6:15 PM 準備出門",
        1: "📅 星期二\n• 大女兒校隊至 5:00 PM\n• 晚上自由時間\n• 💡 建議：親子閱讀或家庭遊戲",
        2: "📅 星期三（半天）\n• 1:00 PM 放學到家\n• 法文堂 / 編程堂 / 數學堂\n• ⚠️ 注意：課外班多，記得準備點心",
        3: "📅 星期四\n• 大女兒校隊至 5:00 PM\n• 晚上自由時間",
        4: "📅 星期五\n• 網球 4:00-5:00 PM\n• 週末前準備\n• 🎉 明天週末了！",
        5: "📅 星期六\n• 週末休息模式\n• 💡 建議：AI閱讀 / 親子活動 / 戶外\n• 小紅書：週末早晨儀式主題",
        6: "📅 星期日\n• 週末休息模式\n• 💡 建議：家庭聚餐 / 下週準備\n• 小紅書：週日晚安/下週預覽主題"
    }
    return schedules.get(weekday, "📅 今日日程")

def generate_report():
    today = datetime.now().strftime('%Y年%m月%d日')
    weekday_names = ['一', '二', '三', '四', '五', '六', '日']
    weekday = weekday_names[datetime.now().weekday()]
    
    schedule = get_schedule()
    
    lines = []
    lines.append(f"📋 <b>Hugo Sammie 家族日報</b>")
    lines.append(f"📅 {today} 星期{weekday}")
    lines.append("")
    lines.append("<b>【今日行程】</b>")
    lines.append(schedule)
    lines.append("")
    lines.append("<b>【投資快訊】</b>")
    lines.append("• 請查看盤前簡報 (晚上 8:30)")
    lines.append("")
    lines.append("<i>💬 需要協助請直接回覆小GoGo</i>")
    
    return "\n".join(lines)

def main():
    report = generate_report()
    send_telegram(report, CHAT_ID)
    send_telegram(report, GROUP_ID)
    print("日程推送完成")

if __name__ == "__main__":
    main()
