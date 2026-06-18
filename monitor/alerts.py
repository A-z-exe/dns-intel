import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message: str) -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not set in .env")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False


def alert_changes(domain: str, changes: dict):
    if not changes["added"] and not changes["removed"]:
        return

    lines = [f"🔔 *DNS Change Detected*\n🌐 Domain: `{domain}`\n"]

    if changes["added"]:
        lines.append("*✅ Added:*")
        for item in changes["added"]:
            lines.append(f"  `+ {item}`")

    if changes["removed"]:
        lines.append("\n*❌ Removed:*")
        for item in changes["removed"]:
            lines.append(f"  `- {item}`")

    lines.append(f"\n⏰ {changes.get('latest_timestamp', '')}")
    message = "\n".join(lines)
    send_telegram(message)
