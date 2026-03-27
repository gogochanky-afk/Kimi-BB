#!/usr/bin/env python3
"""
Hugo Sammie 家族日程自動推送 v2
每天早上 7:45 發送當日行程（私人群組雙推送）
"""

import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# 如果環境變量沒有，使用硬編碼群組 ID
GROUP_ID = os.getenv('TELEGRAM_GROUP_ID', '-5153249366')

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
    """獲取當日日程"""
    today = datetime.now()
    weekday = today.weekday()
    date_str = today.strftime('%m月%d日')
    weekday_names = ['一', '二', '三', '四', '五', '六', '日']
    
    # 日程表
    schedules = {
        0: {  # 星期一
            'morning': '大女兒校隊至 5:00 PM',
            'evening': '中國樂器 6:45-8:00 PM',
            'note': '記得帶樂器'
        },
        1: {  # 星期二
            'morning': '大女兒校隊至 5:00 PM',
            'evening': '晚上自由時間',
            'note': '可以安排家庭活動'
        },
        2: {  # 星期三
            'morning': '半天課 (1:00 PM 放學)',
            'afternoon': '法文/編程/數學堂',
            'note': '接孩子時間較早'
        },
        3: {  # 星期四
            'morning': '大女兒校隊至 5:00 PM',
            'evening': '晚上自由時間',
            'note': '檢查本週功課'
        },
        4: {  # 星期五
            'morning': '正常上課',
            'afternoon': '網球 4:00-5:00 PM',
            'note': '帶網球裝備！'
        },
        5: {  # 星期六
            'morning': '週末家庭時間',
            'note': '可以安排戶外活動'
        },
        6: {  # 星期日
            'morning': '週末休息',
            'note': '準備下週，晚上有閱讀計劃推送'
        }
    }
    
    return date_str, weekday_names[weekday], schedules.get(weekday, {})

def main():
    date_str, weekday, schedule = get_schedule()
    
    lines = []
    lines.append(f"📋 <b>Hugo Sammie 家庭日程</b>")
    lines.append(f"📅 {date_str} 星期{weekday}")
    lines.append("")
    
    if 'morning' in schedule:
        lines.append(f"🌅 上午：{schedule['morning']}")
    if 'afternoon' in schedule:
        lines.append(f"☀️ 下午：{schedule['afternoon']}")
    if 'evening' in schedule:
        lines.append(f"🌙 晚上：{schedule['evening']}")
    
    lines.append("")
    lines.append(f"💡 <b>提醒：</b>{schedule.get('note', '')}")
    lines.append("")
    lines.append("<i>☕ 祝你有美好的一天！</i>")
    
    report = "\n".join(lines)
    
    # 推送到私人聊天
    send_telegram(report, CHAT_ID)
    print(f"已推送到私人: {CHAT_ID}")
    
    # 推送到群組
    send_telegram(report, GROUP_ID)
    print(f"已推送到群組: {GROUP_ID}")

if __name__ == "__main__":
    main()
