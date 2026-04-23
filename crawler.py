import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz

def get_warrants():
    # 設定台灣時區
    tw_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tw_tz)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    stocks = []

    # 1. 經濟日報 - 權證特區
    try:
        res = requests.get("https://money.udn.com/money/cate/5595", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('.story__content')[:12]:
            title = item.select_one('h3 a').text.strip()
            link = "https://money.udn.com" + item.select_one('h3 a')['href']
            # 自動判斷多空
            is_bull = any(word in title for word in ["認購", "看好", "多", "漲", "紅", "旺"])
            stocks.append({
                "id": "UDN", "name": "經濟報", "direction": "bull" if is_bull else "bear",
                "title": title[:22], "reason": title, "source": "udn", "sourceName": "經濟日報",
                "date": now.strftime("%m/%d"), "time": now.strftime("%H:%M"), "link": link
            })
    except Exception as e: print(f"UDN Error: {e}")

    # 2. 工商時報 - 權證
    try:
        res = requests.get("https://www.ctee.com.tw/category/warrant", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('.card-main')[:12]:
            title = item.select_one('.card-title a').text.strip()
            link = item.select_one('.card-title a')['href']
            is_bull = any(word in title for word in ["認購", "看好", "多", "漲", "強", "優"])
            stocks.append({
                "id": "CTEE", "name": "工商報", "direction": "bull" if is_bull else "bear",
                "title": title[:22], "reason": title, "source": "ctee", "sourceName": "工商時報",
                "date": now.strftime("%m/%d"), "time": now.strftime("%H:%M"), "link": link
            })
    except Exception as e: print(f"CTEE Error: {e}")

    # 儲存結果
    output = {
        "lastUpdate": now.strftime("%Y/%m/%d %H:%M"),
        "stocks": stocks
    }
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_warrants()
