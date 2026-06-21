import requests
import os
from datetime import datetime, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DART_API_KEY = os.environ["DART_API_KEY"]

today = datetime.today()
yesterday = today - timedelta(days=1)

bgn = yesterday.strftime("%Y%m%d")
end = today.strftime("%Y%m%d")

url = "https://opendart.fss.or.kr/api/list.json"

params = {
    "crtfc_key": DART_API_KEY,
    "bgn_de": bgn,
    "end_de": end,
    "page_count": 100
}

r = requests.get(url, params=params)
data = r.json()

msg = "🔔 Fund Radar\n\n"

if data["status"] == "000":

    keywords = [
        "집합투자",
        "ETF",
        "증권신고서",
        "효력발생",
        "투자설명서"
    ]

    found = False

    for item in data["list"]:

        title = item["report_nm"]

        if any(k in title for k in keywords):

            found = True

            msg += (
                f"운용사 : {item['corp_name']}\n"
                f"공시 : {title}\n"
                f"날짜 : {item['rcept_dt']}\n\n"
            )

    if not found:
        msg += "신규 펀드 관련 공시가 없습니다."

else:

    msg += "DART 조회 실패"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

print(msg)
