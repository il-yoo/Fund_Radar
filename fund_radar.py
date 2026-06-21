import requests
import os
from datetime import datetime, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DART_API_KEY = os.environ["DART_API_KEY"]

# 날짜
today = datetime.today()
yesterday = today - timedelta(days=3)

bgn = yesterday.strftime("%Y%m%d")
end = today.strftime("%Y%m%d")

# DART 공시 검색
url = "https://opendart.fss.or.kr/api/list.json"

params = {
    "crtfc_key": DART_API_KEY,
    "bgn_de": bgn,
    "end_de": end,
    "page_count": 100
}

r = requests.get(url, params=params)
data = r.json()

message = "🔔 Fund Radar\n\n"

# 신규 펀드 관련 키워드
keywords = [
    "집합투자",
    "증권신고서",
    "효력발생",
    "ETF",
    "투자설명서"
]

results = []

if data.get("status") == "000":

    for item in data["list"]:

        title = item.get("report_nm", "")
        corp = item.get("corp_name", "")
        date = item.get("rcept_dt", "")

        if any(k in title for k in keywords):

            results.append(
                f"운용사 : {corp}\n"
                f"공시 : {title}\n"
                f"접수일 : {date}\n"
            )

if results:

    message += "\n----------------\n".join(results)

else:

    message += "최근 신규 펀드 관련 공시가 없습니다."

# 텔레그램 발송

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
