# Hyperliquid Multi-Position Bot

Automated multi-position trading bot for Hyperliquid.  
Each position can have its own conditional closing logic (MACD, RSI, etc).

## Setup
1. Clone the repo and install dependencies:
   pip install -r requirements.txt
2. Edit config.yaml with your API keys and strategies.
3. Run:
   python main.py

## Notes
- Always test on testnet before mainnet.
- Each job defines its own conditional rule in config.yaml.
- Add new indicator functions in indicators.py.
