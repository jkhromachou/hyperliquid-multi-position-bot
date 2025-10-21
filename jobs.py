from datetime import datetime

class PositionJob:
    def __init__(self, asset, side, entry_price, rule):
        self.asset = asset
        self.side = side
        self.entry_price = entry_price
        self.rule = rule
        self.triggered = False
        self.closed = False
        self.open_size = None
        self.entry_time = datetime.utcnow()

    def __repr__(self):
        return f"<Job {self.asset} {self.side} rule={self.rule.__name__}>"
