import time, yaml, pandas as pd
from indicators import macd_cross_below_minus40, rsi_above_70
from api_client import HyperliquidClient
from jobs import PositionJob
from utils import setup_logger, send_webhook_message

with open("config.yaml") as f:
    config = yaml.safe_load(f)

logger = setup_logger(config["settings"]["log_file"])
api = config["api"]
webhooks = config.get("webhooks", {})
settings = config["settings"]

client = HyperliquidClient(api["url"], api["account_address"], api["secret_key"])

rule_map = {
    "macd_cross_below_minus40": macd_cross_below_minus40,
    "rsi_above_70": rsi_above_70
}

jobs = [
    PositionJob(j["asset"], j["side"], j["entry_price"], rule_map[j["rule"]])
    for j in config["positions"]
]

client.start_price_stream([j.asset for j in jobs])

def main_loop():
    logger.info("Bot started.")
    send_webhook_message("🚀 Bot started.", webhooks.get("discord"), webhooks.get("slack"))

    while True:
        for job in jobs:
            if job.closed:
                continue
            try:
                # Example indicator trigger from price stream (placeholder):
                prices = pd.Series([client.latest_prices.get(job.asset, job.entry_price)])
                if job.rule(prices):
                    msg = f"🔔 Triggered close for {job.asset} ({job.rule.__name__})"
                    logger.info(msg)
                    send_webhook_message(msg, webhooks.get("discord"), webhooks.get("slack"))

                    positions = client.fetch_positions()
                    for p in positions:
                        if p["position"]["coin"] == job.asset:
                            size = float(p["position"]["szi"])
                            client.close_position(job.asset, job.side, size)
                            job.closed = True
                            break
            except Exception as e:
                logger.error(f"Error with {job.asset}: {e}")
        time.sleep(settings["poll_interval"])

if __name__ == "__main__":
    main_loop()
