#!/usr/bin/env python3
"""
Notion 整合模組 - Hugo Sammie 家族辦公室知識庫
用途：讀取投資決策、家庭會議紀要、寫入每日摘要
"""

import os
import json
import urllib.request
from datetime import datetime

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

def notion_api(endpoint, method='GET', data=None):
    """呼叫 Notion API"""
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    try:
        req = urllib.request.Request(url, method=method)
        for key, value in headers.items():
            req.add_header(key, value)
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Notion API 錯誤: {e}")
        return None

def get_investment_decisions():
    """讀取最近的投資決策記錄"""
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return []
    
    data = {
        "filter": {
            "property": "Type",
            "select": {"equals": "投資決策"}
        },
        "sorts": [{"timestamp": "created_time", "direction": "descending"}],
        "page_size": 5
    }
    
    result = notion_api(f'databases/{NOTION_DATABASE_ID}/query', 'POST', data)
    if result and 'results' in result:
        decisions = []
        for page in result['results']:
            props = page.get('properties', {})
            title = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '未命名')
            decisions.append(title)
        return decisions
    return []

def add_daily_summary(content):
    """寫入每日摘要到 Notion"""
    if not NOTION_TOKEN:
        return False
    
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": f"每日摘要 {datetime.now().strftime('%Y-%m-%d')}"}}]},
            "Type": {"select": {"name": "每日摘要"}},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    }
    
    result = notion_api('pages', 'POST', data)
    return result is not None

def get_family_meeting_notes():
    """讀取最近的家庭會議紀要"""
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return []
    
    data = {
        "filter": {
            "property": "Type",
            "select": {"equals": "家庭會議"}
        },
        "sorts": [{"timestamp": "created_time", "direction": "descending"}],
        "page_size": 3
    }
    
    result = notion_api(f'databases/{NOTION_DATABASE_ID}/query', 'POST', data)
    if result and 'results' in result:
        notes = []
        for page in result['results']:
            props = page.get('properties', {})
            title = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '未命名')
            notes.append(title)
        return notes
    return []

if __name__ == "__main__":
    # 測試
    print("測試 Notion 連接...")
    decisions = get_investment_decisions()
    print(f"最近投資決策: {decisions}")
    
    meetings = get_family_meeting_notes()
    print(f"最近家庭會議: {meetings}")
