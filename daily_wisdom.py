#!/usr/bin/env python3
"""
Hugo Sammie 每日智識推送系統
每天早上 8:00 推送一本實用書籍精華
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

# 智識庫：100本實用書籍精華（預製內容，零日後成本）
KNOWLEDGE_BASE = [
    {
        "title": "《原子習慣》",
        "author": "詹姆斯·克利爾",
        "category": "效率習慣",
        "core": "每天進步1%，一年後會進步37倍。關鍵不在目標，而在「系統」。",
        "insights": [
            "讓好習慣「顯而易見」- 環境設計比意志力重要",
            "讓壞習慣「困難重重」- 增加摩擦，自然減少",
            "「身份認同」改變 - 不是「我想戒煙」，是「我不抽煙」"
        ],
        "application": "投資：建立固定檢視系統，而非追求單次獲利。孩子：幫孩子建立「閱讀身份」而非逼他讀書。",
        "action": "找出一件想改變的小事，設計環境讓它自動發生"
    },
    {
        "title": "《窮查理的普通常識》",
        "author": "查理·芒格",
        "category": "投資理財",
        "core": "多元思維模型：投資不只看財報，要懂心理學、物理學、歷史、數學。",
        "insights": [
            "反過來想，總是反過來想 - 先想怎樣會失敗",
            "能力圈原則 - 只投資你懂的，不懂的不碰",
            "人類誤判心理學 - 認清自己的認知偏誤"
        ],
        "application": "投資：檢視持倉是否跨足太多不懂的領域。決策：重大決定前，先列出「為什麼這會失敗」。",
        "action": "選一個持倉，問自己：我真的懂這門生意嗎？"
    },
    {
        "title": "《原則》",
        "author": "雷·達里奧",
        "category": "商業管理",
        "core": "極度透明 + 系統化決策。把原則寫下來，讓決策可复制、可優化。",
        "insights": [
            "痛苦 + 反思 = 進步",
           「激進的真相和激進的透明",
            "系統化決策 - 不要靠直覺，要靠原則"
        ],
        "application": "家族辦公室：建立投資決策流程，不因情緒改變。家庭：和孩子溝通也要「極度透明」。",
        "action": "寫下3條你的投資原則，貼在螢幕旁邊"
    },
    {
        "title": "《快思慢想》",
        "author": "丹尼爾·康納曼",
        "category": "心理認知",
        "core": "大腦有兩個系統：系統1（快思考，直覺）和系統2（慢思考，理性）。",
        "insights": [
            "錨定效應 - 第一個數字會影響所有判斷",
           「損失厭惡 - 損失的痛苦是獲利快樂的2倍",
           「可得性偏誤 - 最近發生的事會被過度高估"
        ],
        "application": "投資：股票跌時別恐慌（損失厭惡），漲時別貪婪（可得性偏誤）。",
        "action": "下次想賣股票時，問自己：是理性分析還是情緒反應？"
    },
    {
        "title": "《從A到A+》",
        "author": "吉姆·柯林斯",
        "category": "商業管理",
        "core": "優秀是卓越的大敵。偉大公司不是靠一次爆發，而是靠持續的紀律。",
        "insights": [
            "第五級領導 - 謙遜 + 意志，不是個人魅力",
           「先找對人，再想做什麼",
           「刺蝟概念 - 只做你最能賺錢、最熱愛、最能做到世界級的事"
        ],
        "application": "投資：找有「第五級領導」的公司。家族：培養孩子謙遜而堅定的品格。",
        "action": "檢視你的持倉：CEO 是第五級領導者嗎？"
    },
    {
        "title": "《富過三代》",
        "author": "詹姆斯·休斯",
        "category": "家族傳承",
        "core": "財富傳承不只是錢，是價值觀、家族文化、人力資本的傳承。",
        "insights": [
            「家族憲法 - 寫下家族的價值觀和決策原則",
           「家族會議 - 定期溝通，讓下一代參與",
           「人力資本 > 金融資本 - 培養孩子比留錢更重要"
        ],
        "application": "開始寫家族憲法初稿。每月一次家庭會議，讓孩子參與決定。",
        "action": "本週和孩子討論：我們家最重視的3個價值是什麼？"
    },
    {
        "title": "《智慧型股票投資人》",
        "author": "班傑明·葛拉漢",
        "category": "投資理財",
        "core": "「市場先生」每天都會報價，但不要被他影響。投資要有安全邊際。",
        "insights": [
            "市場先生比喻 - 情緒化的鄰居，不要被他影響",
           「安全邊際 - 買得夠便宜，就算錯了也不會大虧",
           「區分投資和投機 - 投資看價值，投機看價格"
        ],
        "application": "設立「安全邊際」標準：只買低於內在價值7折的股票。",
        "action": "檢視持倉：每隻股票有沒有安全邊際？"
    },
    {
        "title": "《影響力》",
        "author": "羅伯特·席爾迪尼",
        "category": "心理認知",
        "core": "人類有6大影響力原則：互惠、承諾一致、社會認同、喜好、權威、稀缺。",
        "insights": [
            "互惠原則 - 先給予，再請求",
           「稀缺性 - 限時限量會讓人失去理智",
           「社會認同 - 大家都做，我就跟著做"
        ],
        "application": "投資：識別市場的「社會認同」陷阱（大家都買時要小心）。教育：用「承諾一致」幫孩子建立習慣。",
        "action": "下次聽到「限時優惠」時，警鐘響起，冷靜分析"
    },
    {
        "title": "《搞定》",
        "author": "大衛·艾倫",
        "category": "效率習慣",
        "core": "GTD方法：清空大腦，把所有事情記下來，分類處理。",
        "insights": [
            "收集 - 所有事情進收件匣，不要放在腦中",
           「下一步行動 - 每個項目都要有具體的下一步",
           「每週回顧 - 清理、更新、檢視所有項目"
        ],
        "application": "建立家族辦公室的GTD系統：投資決策、家庭事務、孩子活動都進系統。",
        "action": "今天把腦中所有待辦寫下來，分類處理"
    },
    {
        "title": "《槍炮、病菌與鋼鐵》",
        "author": "賈德·戴蒙",
        "category": "宏觀思維",
        "core": "地理環境決定文明發展，不是種族優劣。理解大歷史，預測大趨勢。",
        "insights": [
            「地理決定論 - 可馴化動植物多的地區發展快",
           「病菌的作用 - 征服者帶來的病菌比武器更致命",
           「技術傳播 - 東西向大陸比南北向更易傳播技術"
        ],
        "application": "投資：理解宏觀趨勢（如AI、氣候變化）比選股更重要。",
        "action": "思考：未來20年，哪些「地理因素」會改變世界格局？"
    }
    # 可擴展至100本...
]

def get_today_book():
    """根據日期輪換書籍"""
    day_of_year = datetime.now().timetuple().tm_yday
    index = (day_of_year - 1) % len(KNOWLEDGE_BASE)
    return KNOWLEDGE_BASE[index]

def generate_daily_wisdom():
    """生成每日智識"""
    book = get_today_book()
    today = datetime.now().strftime('%m月%d日')
    
    lines = []
    lines.append(f"📚 <b>小GoGo 每日智識 ({today})</b>")
    lines.append("")
    lines.append(f"📖 {book['title']}")
    lines.append(f"✍️ {book['author']} | 🏷️ {book['category']}")
    lines.append("")
    
    lines.append("<b>【核心思想】</b>")
    lines.append(book['core'])
    lines.append("")
    
    lines.append("<b>【3個 actionable insights】</b>")
    for i, insight in enumerate(book['insights'], 1):
        lines.append(f"{i}. {insight}")
    lines.append("")
    
    lines.append("<b>【應用到家族辦公室】</b>")
    lines.append(book['application'])
    lines.append("")
    
    lines.append("<b>【今日實踐】</b>")
    lines.append(f"□ {book['action']}")
    lines.append("")
    
    lines.append("<i>💡 每天一本書，一年智識升級。明天見！</i>")
    
    return "\n".join(lines)

def main():
    report = generate_daily_wisdom()
    send_telegram(report, CHAT_ID)
    send_telegram(report, GROUP_ID)
    print("每日智識推送完成")

if __name__ == "__main__":
    main()
