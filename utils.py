import json, requests, logging

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("hyperliquid_bot")

def send_webhook_message(msg, discord_url=None, slack_url=None):
    payload = {"content": msg}
    if discord_url:
        try:
            requests.post(discord_url, json=payload, timeout=5)
        except Exception:
            pass
    if slack_url:
        try:
            requests.post(slack_url, json={"text": msg}, timeout=5)
        except Exception:
            pass
