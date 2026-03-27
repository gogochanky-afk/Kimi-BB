#!/usr/bin/env python3
"""
Hugo Sammie 全球晨報
每天早上 9:00 推送世界新聞 + 機會 + 知識
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

def generate_news_report():
    """生成晨報（簡化版，實際可擴展 RSS 抓取）"""
    today = datetime.now().strftime('%m月%d日')
    weekday = ['一', '二', '三', '四', '五', '六', '日'][datetime.now().weekday()]
    
    lines = []
    lines.append(f"📰 <b>Hugo Sammie 全球晨報</b>")
    lines.append(f"📅 {today} 星期{weekday}")
    lines.append("")
    
    # 世界熱點（這裡可以擴展 RSS 抓取）
    lines.append("<b>🌍 【世界熱點】</b>")
    lines.append("• 美聯儲政策動態 - 關注今晚官員講話")
    lines.append("• 亞洲市場開盤 - 日經/恆生指數")
    lines.append("• 地緣政治 - 中東/烏克蘭局勢")
    lines.append("")
    
    # 投資機會
    lines.append("<b>💰 【投資機會】</b>")
    lines.append("• 科技股：AI 應用落地加速")
    lines.append("• 新能源：政策持續利好")
    lines.append("• 關注：本週美國 GDP 數據")
    lines.append("")
    
    # 今日日程提醒
    lines.append("<b>📋 【今日提醒】</b>")
    lines.append("• 晚上 8:30 - 美股盤前簡報")
    lines.append("• 晚上 10:30 - 開盤機會檢查")
    lines.append("")
    
    # 知識充電
    lines.append("<b>📚 【今日知識】</b>")
    lines.append("主題：家族辦公室的風險管理")
    lines.append("💡 分散投資不只是買不同股票，")
    lines.append("   還要考慮地域、幣種、資產類別")
    lines.append("")
    
    lines.append("<i>☕ 祝你有美好的一天！有問題隨時問小GoGo</i>")
    
    return "\n".join(lines)

def main():
    report = generate_news_report()
    send_telegram(report, CHAT_ID)
    send_telegram(report, GROUP_ID)
    print("晨報推送完成")

if __name__ == "__main__":
    main()

