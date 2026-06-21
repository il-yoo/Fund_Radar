import requests
import os
from datetime import datetime, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DART_API_KEY = os.environ["DART_API_KEY"]


def is_fund_disclosure(title):

    # 반드시 집합투자증권 포함
    if "집합투자증권" not in title:
        return False

    # 제외할 공시
    exclude = [
        "채무증권",
        "주식",
        "파생결합",
        "정정"
    ]

    if any(x in title for x in exclude):
        return False

    # 포함할 공시
    include = [
        "증권신고서",
        "효력발생",
        "투자설명서"
    ]

    return any(x in title for x in include)


# 최근 3일 조회
today = datetime.today()
start_day = today - timedelta(days=3)

bgn = start_day.strftime("%Y%m%d")
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

message = "🔔 Fund Radar\n\n"

results = []

if data.get("status") == "000":

    for item in data.get("list", []):

        title = item.get("report_nm", "")
        corp = item.get("corp_name", "")
        date = item.get("rcept_dt", "")

        if is_fund_disclosure(title):

            icon = "🔹"

            if "효력발생" in title:
                icon = "🟢"

            elif "증권신고서" in title:
                icon = "🟡"

            results.append(
                f"{icon} 신규 집합투자증권 공시\n"
                f"운용사 : {corp}\n"
                f"공시명 : {title}\n"
                f"접수일 : {date}\n"
            )

if results:

    message += "\n----------------------\n".join(results)

else:

    message += "최근 집합투자증권 신규 공시가 없습니다."


telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
