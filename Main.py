import os
import requests
import json
import time

# Slack Webhook for alerts
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Token and DEX setup
token = "ETH"
dex_1_name = "Uniswap"
dex_2_name = "SushiSwap"

# Simulated live price fetch using CoinGecko API (can replace with on-chain API for production)
def fetch_token_price(dex):
    if dex == "Uniswap":
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
    elif dex == "SushiSwap":
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
    else:
        return None
    return response.json()["ethereum"]["usd"]

# Calculate arbitrage
def calculate_arbitrage():
    buy_price = fetch_token_price(dex_1_name)
    sell_price = fetch_token_price(dex_2_name)
    if buy_price and sell_price:
        net_profit = sell_price - buy_price
        return buy_price, sell_price, net_profit
    return None, None, None

# Slack alert
def send_slack_alert(message):
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})

# MAIN SCRIPT
if __name__ == "__main__":
    print("ð Arbitrage bot started with Tier 10 upgrades...")
    buy_price, sell_price, net_profit = calculate_arbitrage()

    if buy_price and sell_price:
        print(f"Token: {token}")
        print(f"Buy from {dex_1_name}: ${buy_price}")
        print(f"Sell on {dex_2_name}: ${sell_price}")
        print(f"Net Profit: ${net_profit:.2f}")

        if net_profit > 0:
            message = (
                f"â Arbitrage Opportunity Detected!
"
                f"Buy from {dex_1_name} at ${buy_price}
"
                f"Sell on {dex_2_name} at ${sell_price}
"
                f"Estimated Profit: ${net_profit:.2f}"
            )
            send_slack_alert(message)
    else:
        print("Failed to retrieve prices. Retrying in next deployment.")
