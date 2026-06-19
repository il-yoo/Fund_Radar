import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
🔔 Fund Radar 테스트 성공!

✅ GitHub Actions 정상
✅ Telegram 연동 성공
✅ DART API Secret 등록 완료

다음 단계부터 신규 펀드 탐색을 시작합니다.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Telegram message sent.")
