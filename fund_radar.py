import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
DART_API_KEY = os.environ["DART_API_KEY"]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


def get_recent_disclosures():

    url = "https://opendart.fss.or.kr/api/list.json"

    params = {
        "crtfc_key": DART_API_KEY,
        "bgn_de": "20260617",
        "end_de": "20260618",
        "page_count": 100
    }

    r = requests.get(url, params=params)

    data = r.json()

    if data.get("status") != "000":
        return []

    result = []

    keywords = [
        "집합투자",
        "증권신고서",
        "ETF",
        "효력발생",
        "투자설명서"
    ]

    for item in data["list"]:

        title = item.get("report_nm", "")

        if any(k in title for k in keywords):

            result.append({
                "corp": item.get("corp_name"),
                "title": title,
                "date": item.get("rcept_dt")
            })

    return result


def main():

    funds = get_recent_disclosures()

    if not funds:

        send_telegram("📢 오늘 신규 펀드 관련 공시가 없습니다.")
        return

    msg = "🔔 Fund Radar\n\n"

    for f in funds:

        msg += f"운용사 : {f['corp']}\n"
        msg += f"공시명 : {f['title']}\n"
        msg += f"접수일 : {f['date']}\n"
        msg += "------------------\n"

    send_telegram(msg)


if __name__ == "__main__":
    main()
