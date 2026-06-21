import requests
import os
from datetime import datetime, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DART_API_KEY = os.environ["DART_API_KEY"]


def classify(title):

    if title.startswith("증권신고서(집합투자증권"):

        return (
            "🟡 신규 집합투자증권",
            "D+3 ~ D+7"
        )

    if "집합투자증권" in title and "효력발생" in title:

        return (
            "🟢 설정 임박",
            "오늘 ~ 내일"
        )

    if "집합투자증권" in title and "투자설명서" in title:

        return (
            "🔵 판매 개시",
            "D+0 ~ D+2"
        )

    return None


today = datetime.today()

start = today - timedelta(days=5)


params = {

    "crtfc_key": DART_API_KEY,

    "bgn_de": start.strftime("%Y%m%d"),

    "end_de": today.strftime("%Y%m%d"),

    "page_count": 100

}


url = "https://opendart.fss.or.kr/api/list.json"


r = requests.get(url, params=params)

data = r.json()


message = "🔔 Fund Radar 2.1\n\n"


results = []


if data.get("status") == "000":

    for item in data["list"]:

        title = item["report_nm"]

        info = classify(title)


        if info:

            status, eta = info

            corp = item["corp_name"]

            date = item["rcept_dt"]

            rcept_no = item["rcept_no"]


            dart_link = (

                "https://dart.fss.or.kr/dsaf001/main.do?"

                f"rcpNo={rcept_no}"

            )


            results.append(

                f"{status}\n\n"

                f"운용사 : {corp}\n"

                f"공시 : {title}\n"

                f"접수일 : {date}\n"

                f"예상설정 : {eta}\n\n"

                f"공시보기\n{dart_link}"

            )


if results:

    message += "\n\n━━━━━━━━━━\n\n".join(results)

else:

    message += "최근 집합투자증권 신규 공시가 없습니다."


telegram_url = (

    f"https://api.telegram.org/bot"

    f"{BOT_TOKEN}/sendMessage"

)


requests.post(

    telegram_url,

    data={

        "chat_id": CHAT_ID,

        "text": message,

        "disable_web_page_preview": True

    }

)


print(message)
