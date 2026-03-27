#!/usr/bin/env python3
"""
Hugo Sammie 智能市場監控系統 v2.0
分級推送：P0緊急 / P1重要 / P2一般
"""

import yfinance as yf
import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')

PORTFOLIO = {
    '核心': ['MSFT', 'NVDA', 'GOOGL', 'AAPL'],
    '黑馬': ['OKLO', 'CRDO', 'TPL', 'SEZL', 'WGS'],
    '指數': ['QQQ', 'SPY', 'DIA', 'VIX']
}

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

def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        if len(hist) < 2:
            return None
        
        latest = hist.iloc[-1]
        prev = hist.iloc[-2]
        change_pct = (latest['Close'] - prev['Close']) / prev['Close'] * 100
        volume_ratio = latest['Volume'] / hist['Volume'].mean()
        
        # 計算RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        
        return {
            'symbol': symbol,
            'price': round(latest['Close'], 2),
            'change_pct': round(change_pct, 2),
            'volume_ratio': round(volume_ratio, 1),
            'rsi': round(current_rsi, 1),
            'high_20d': round(hist['Close'].max(), 2),
            'low_20d': round(hist['Close'].min(), 2)
        }
    except:
        return None

def classify_alert(data):
    """分級警報系統"""
    alerts = []
    
    # P0 - 緊急（任何時間推送）
    if abs(data['change_pct']) > 5:
        alerts.append(('P0', f"🚨 劇烈波動 {data['change_pct']:+.1f}%"))
    if data['price'] >= data['high_20d']:
        alerts.append(('P0', f"🔥 20日新高"))
    if data['price'] <= data['low_20d']:
        alerts.append(('P0', f"❄️ 20日新低"))
    if data['volume_ratio'] > 5:
        alerts.append(('P0', f"⚡ 成交量暴增 {data['volume_ratio']:.1f}倍"))
    
    # P1 - 重要（統一時間推送）
    if abs(data['change_pct']) > 3 and not alerts:
        alerts.append(('P1', f"📊 明顯波動 {data['change_pct']:+.1f}%"))
    if data['rsi'] > 70:
        alerts.append(('P1', f"⚠️ RSI超買 {data['rsi']:.0f}"))
    if data['rsi'] < 30:
        alerts.append(('P1', f"💡 RSI超賣 {data['rsi']:.0f}"))
    if data['volume_ratio'] > 2:
        alerts.append(('P1', f"📈 放量 {data['volume_ratio']:.1f}倍"))
    
    # P2 - 一般（盤後總結）
    if abs(data['change_pct']) > 2 and not alerts:
        alerts.append(('P2', f"波動 {data['change_pct']:+.1f}%"))
    
    return alerts

def generate_premarket_report():
    """盤前簡報（晚上 8:30）"""
    lines = ["📊 <b>美股盤前預覽</b>", f"🕐 {datetime.now().strftime('%m月%d日 %H:%M')}", ""]
    
    p0_alerts = []
    p1_alerts = []
    
    for category, symbols in PORTFOLIO.items():
        for symbol in symbols:
            data = get_stock_data(symbol)
            if data:
                alerts = classify_alert(data)
                for level, desc in alerts:
                    if level == 'P0':
                        p0_alerts.append(f"{symbol}: {desc}")
                    elif level == 'P1':
                        p1_alerts.append(f"{symbol}: {desc}")
    
    # 如果有 P0，立即標註
    if p0_alerts:
        lines.append("🚨 <b>【緊急關注】</b>")
        for alert in p0_alerts[:3]:  # 最多顯示3個
            lines.append(f"• {alert}")
        lines.append("")
    
    # P1 摘要
    if p1_alerts:
        lines.append(f"📋 <b>【今日關注】</b> 共 {len(p1_alerts)} 項異動")
        for alert in p1_alerts[:5]:
            lines.append(f"• {alert}")
        lines.append("")
    
    lines.append("💬 <i>小GoGo 10:30 PM 再看盤，有機會即時推您</i>")
    return "\n".join(lines)

def check_opportunities():
    """開盤後機會檢查（晚上 10:30）"""
    opportunities = []
    
    for category, symbols in PORTFOLIO.items():
        for symbol in symbols:
            data = get_stock_data(symbol)
            if data:
                alerts = classify_alert(data)
                p0_count = sum(1 for level, _ in alerts if level == 'P0')
                p1_count = sum(1 for level, _ in alerts if level == 'P1')
                
                if p0_count > 0 or p1_count > 0:
                    opportunities.append({
                        'symbol': symbol,
                        'data': data,
                        'p0': p0_count,
                        'p1': p1_count
                    })
    
    if not opportunities:
        return None  # 沒有機會就不推送
    
    # 按重要性排序
    opportunities.sort(key=lambda x: (x['p0'], x['p1']), reverse=True)
    
    lines = ["🎯 <b>開盤機會警報</b>", f"🕐 {datetime.now().strftime('%H:%M')}", ""]
    
    for opp in opportunities[:3]:  # 最多3個
        data = opp['data']
        emoji = "🚨" if opp['p0'] > 0 else "📊"
        lines.append(f"{emoji} <b>{data['symbol']}</b> ${data['price']} ({data['change_pct']:+.1f}%)")
        lines.append(f"   RSI: {data['rsi']} | 成交量: {data['volume_ratio']}倍")
        lines.append("")
    
    lines.append("<i>💡 詳細分析請問小GoGo</i>")
    return "\n".join(lines)

def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'premarket'
    
    if mode == 'premarket':
        # 晚上 8:30 盤前預覽
        report = generate_premarket_report()
        send_telegram(report, CHAT_ID)
        send_telegram(report, GROUP_ID)
        
    elif mode == 'opportunity':
        # 晚上 10:30 機會檢查
        report = check_opportunities()
        if report:  # 有機會才推送
            send_telegram(report, CHAT_ID)
            send_telegram(report, GROUP_ID)
        else:
            print("無重要機會，跳過推送")

if __name__ == "__main__":
    main()

