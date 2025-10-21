import time
from hyperliquid import Exchange, Info
from hyperliquid.utils import constants

class HyperliquidClient:
    def __init__(self, api_url, account_address, secret_key):
        self.info = Info(api_url, skip_ws=True)
        self.exchange = Exchange(api_url, account_address, secret_key)
        self.address = account_address

    def fetch_positions(self):
        state = self.info.user_state(self.address)
        return state.get("assetPositions", [])

    def fetch_candles(self, asset, lookback=200):
        # Placeholder — fetch 4h candles from market data endpoint
        # Replace with API call for real data
        return []

    def close_position(self, asset, side, size):
        is_buy = (side == "short")
        order_body = {
            "action": {
                "type": "order",
                "orders": [{
                    "a": constants.ASSET_INDEX(asset),
                    "b": is_buy,
                    "p": "0",
                    "s": str(size),
                    "r": True,
                    "t": {"market": {}}
                }],
                "grouping": "na"
            },
            "nonce": int(time.time() * 1000)
        }
        return self.exchange.place_order(order_body)
