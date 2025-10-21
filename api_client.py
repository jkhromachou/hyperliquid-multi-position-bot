import time, json, websocket, threading
from hyperliquid import Exchange, Info
from hyperliquid.utils import constants

class HyperliquidClient:
    def __init__(self, api_url, account_address, secret_key):
        self.info = Info(api_url, skip_ws=True)
        self.exchange = Exchange(api_url, account_address, secret_key)
        self.address = account_address
        self.ws_url = "wss://api.hyperliquid.xyz/ws"

        self.latest_prices = {}  # {asset: last price}

    def fetch_positions(self):
        state = self.info.user_state(self.address)
        return state.get("assetPositions", [])

    def start_price_stream(self, assets):
        """Connect websocket and stream price updates for specified assets."""
        def run_ws():
            ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=lambda ws, msg: self._on_message(json.loads(msg))
            )
            # subscribe to tickers
            sub_msg = {"type": "subscribe", "channels": [{"name": "ticker", "symbols": assets}]}
            ws.on_open = lambda ws: ws.send(json.dumps(sub_msg))
            ws.run_forever()

        threading.Thread(target=run_ws, daemon=True).start()

    def _on_message(self, msg):
        if msg.get("channel") == "ticker":
            for tick in msg.get("data", []):
                symbol = tick.get("coin")
                price = float(tick.get("markPx", 0))
                self.latest_prices[symbol] = price

    def close_position(self, asset, side, size):
        is_buy = (side == "short")  # short closes by buying
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
