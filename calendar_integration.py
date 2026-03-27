#!/usr/bin/env python3
"""
Google Calendar 整合模組
用途：讀取家庭日程、投資日曆、學校活動
"""

import os
import json
import urllib.request
from datetime import datetime, timedelta

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')  # 家族日曆ID

def get_calendar_events():
    """獲取今日和明日的日曆事件"""
    if not GOOGLE_API_KEY or not GOOGLE_CALENDAR_ID:
        return []
    
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    
    # 時間範圍：今天到明天
    time_min = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_max = tomorrow.strftime('%Y-%m-%dT23:59:59Z')
    
    url = f"https://www.googleapis.com/calendar/v3/calendars/{GOOGLE_CALENDAR_ID}/events"
    params = f"?key={GOOGLE_API_KEY}&timeMin={time_min}&timeMax={time_max}&orderBy=startTime&singleEvents=true"
    
    try:
        req = urllib.request.Request(url + params)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            events = data.get('items', [])
            
            formatted_events = []
            for event in events:
                start = event.get('start', {})
                # 處理全天事件和時間事件
                if 'dateTime' in start:
                    time_str = start['dateTime'][11:16]  # 提取 HH:MM
                else:
                    time_str = "全天"
                
                formatted_events.append({
                    'time': time_str,
                    'summary': event.get('summary', '無標題'),
                    'description': event.get('description', '')
                })
            
            return formatted_events
    except Exception as e:
        print(f"Calendar API 錯誤: {e}")
        return []

def get_today_schedule_text():
    """生成今日日程文字（替代硬編碼）"""
    events = get_calendar_events()
    
    if not events:
        return "📅 今日無特別安排，享受自由時間！"
    
    lines = ["📅 <b>今日家庭日程</b>", ""]
    
    for event in events:
        lines.append(f"⏰ {event['time']} - {event['summary']}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    # 測試
    print("測試 Google Calendar 連接...")
    schedule = get_today_schedule_text()
    print(schedule)
