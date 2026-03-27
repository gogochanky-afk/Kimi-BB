#!/usr/bin/env python3
"""
RSS 新聞整合模組
用途：抓取多個新聞源，生成 9:00 AM 晨報
"""

import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_SOURCES = {
    "BBC 中文": "http://feeds.bbci.co.uk/zhongwen/trad/rss.xml",
    "Reuters": "https://www.reutersagency.com/feed/?taxonomy=markets",
    "TechCrunch": "https://techcrunch.com/feed/",
    "華爾街日報中文": "https://cn.wsj.com/zh-hans/rss",
}

def fetch_rss(url, max_items=3):
    """抓取 RSS 並解析"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            root = ET.fromstring(content)
            
            items = []
            # 處理不同格式的 RSS
            channel = root.find('.//channel') or root
            for item in channel.findall('.//item')[:max_items]:
                title = item.find('title')
                link = item.find('link')
                if title is not None and title.text:
                    items.append({
                        'title': title.text[:100],  # 限制長度
                        'link': link.text if link is not None else ''
                    })
            return items
    except Exception as e:
        print(f"RSS 抓取錯誤 ({url}): {e}")
        return []

def generate_news_briefing():
    """生成新聞簡報"""
    lines = []
    lines.append(f"📰 <b>Hugo Sammie 全球晨報</b>")
    lines.append(f"📅 {datetime.now().strftime('%m月%d日')}")
    lines.append("")
    
    all_news = []
    
    for source, url in RSS_SOURCES.items():
        items = fetch_rss(url, max_items=2)
        if items:
            all_news.append({
                'source': source,
                'items': items
            })
    
    if all_news:
        lines.append("<b>🌍 【世界熱點】</b>")
        for news in all_news[:3]:  # 最多3個來源
            lines.append(f"\n📍 {news['source']}:")
            for item in news['items'][:2]:  # 每個來源2條
                lines.append(f"• {item['title']}")
    else:
        lines.append("<b>🌍 【今日關注】</b>")
        lines.append("• 美聯儲政策動態 - 關注今晚官員講話")
        lines.append("• 亞洲市場開盤概況")
        lines.append("• 地緣政治局勢更新")
    
    lines.append("")
    lines.append("<i>💡 詳細內容請問小GoGo</i>")
    
    return "\n".join(lines)

if __name__ == "__main__":
    # 測試
    print("測試 RSS 新聞抓取...")
    briefing = generate_news_briefing()
    print(briefing)
