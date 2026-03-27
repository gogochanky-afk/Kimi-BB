from http.server import BaseHTTPRequestHandler
import json, urllib.request, urllib.parse, os
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
GROUP_ID = os.environ.get('TELEGRAM_GROUP_ID', '-5153249366')

def send_telegram(message, chat_id):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode()).get('ok', False)
    except Exception as e:
        return False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        today = datetime.now().strftime('%m月%d日')
        lines = [f"📊 <b>美股盘前简报 | {today}</b>", "", "🌙 盘前概况", "• 期指走势跟踪中", "• 开盘前情绪观察", "", "⏰ 今晚安排", "• 10:30 PM - 开盘机会检查", "", "💡 小GoGo提醒", "👀 有重要异动会立即推送", "", "<i>— Hugo Sammie 家族办公室</i>"]
        report = "\n".join(lines)
        send_telegram(report, CHAT_ID)
        send_telegram(report, GROUP_ID)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'success'}).encode())
    def do_POST(self): return self.do_GET()
