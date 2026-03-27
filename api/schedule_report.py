from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
GROUP_ID = os.environ.get('TELEGRAM_GROUP_ID', '-5153249366')

def send_telegram(message, chat_id):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode()).get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_schedule():
    today = datetime.now()
    weekday = today.weekday()
    date_str = today.strftime('%m月%d日')
    weekday_names = ['一', '二', '三', '四', '五', '六', '日']
    schedules = {
        0: {'morning': '大女儿校队至 5:00 PM', 'evening': '中国乐器 6:45-8:00 PM', 'note': '记得带乐器'},
        1: {'morning': '大女儿校队至 5:00 PM', 'evening': '晚上自由时间', 'note': '可以安排家庭活动'},
        2: {'morning': '半天课 (1:00 PM 放学)', 'afternoon': '法文/编程/数学堂', 'note': '接孩子时间较早'},
        3: {'morning': '大女儿校队至 5:00 PM', 'evening': '晚上自由时间', 'note': '检查本周功课'},
        4: {'morning': '正常上课', 'afternoon': '网球 4:00-5:00 PM', 'note': '带网球装备！'},
        5: {'morning': '周末家庭时间', 'note': '可以安排户外活动'},
        6: {'morning': '周末休息', 'note': '准备下周'}
    }
    return date_str, weekday_names[weekday], schedules.get(weekday, {})

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            date_str, weekday, schedule = get_schedule()
            lines = [f"📋 <b>Hugo Sammie 家庭日程</b>", f"📅 {date_str} 星期{weekday}", ""]
            if 'morning' in schedule: lines.append(f"🌅 上午：{schedule['morning']}")
            if 'afternoon' in schedule: lines.append(f"☀️ 下午：{schedule['afternoon']}")
            if 'evening' in schedule: lines.append(f"🌙 晚上：{schedule['evening']}")
            lines.extend(["", f"💡 <b>提醒：</b>{schedule.get('note', '')}", "", "<i>☕ 祝你有美好的一天！</i>"])
            report = "\n".join(lines)
            send_telegram(report, CHAT_ID)
            send_telegram(report, GROUP_ID)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
    def do_POST(self): return self.do_GET()
