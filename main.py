import time
import yaml
import pandas as pd
from indicators import macd_cross_below_minus40, rsi_above_70
from api_client import HyperliquidClient
from jobs import PositionJob

with open("config.yaml") as f:
    config = yaml.safe_load(f)

api = config["api"]
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

def main_loop():
    print("Starting bot...")
    while True:
        for job in jobs:
            if job.closed:
                continue

            candles = client.fetch_candles(job.asset)
            prices = pd.Series([c["close"] for c in candles])
            if job.rule(prices):
                print(f"Triggered close for {job.asset} ({job.rule.__name__})")
                positions = client.fetch_positions()
                for p in positions:
                    if p["position"]["coin"] == job.asset:
                        size = float(p["position"]["szi"])
                        client.close_position(job.asset, job.side, size)
                        job.closed = True
                        break
        time.sleep(settings["poll_interval"])

if __name__ == "__main__":
    main_loop()
