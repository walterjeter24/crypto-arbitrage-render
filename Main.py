import requests

# === CONFIG ===
slack_webhook = "https://hooks.zapier.com/hooks/catch/23548918/ub1tmbk/"
coingecko_url = "https://api.coingecko.com/api/v3/simple/price"
token_id = "ethereum"

# === FETCH PRICE ===
def get_live_price():
    params = {
        "ids": token_id,
        "vs_currencies": "usd"
    }
    try:
        res = requests.get(coingecko_url, params=params)
        data = res.json()
        return float(data[token_id]['usd'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# === SLACK ALERT ===
def send_slack_message(message):
    payload = {"text": message}
    try:
        response = requests.post(slack_webhook, json=payload)
        if response.status_code != 200:
            print(f"Slack error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")

# === SIMULATE ARBITRAGE ===
def simulate_arbitrage():
    live_price = get_live_price()
    if live_price is None:
        return

    uniswap_price = live_price
    sushiswap_price = live_price * 1.014  # Simulated 1.4% higher

    buy_price = uniswap_price
    sell_price = sushiswap_price
    net_profit = sell_price - buy_price

    print("🚀 Arbitrage bot started...")
    print(f"Live Price: ${live_price:.2f}")
    print(f"Buy on Uniswap: ${buy_price:.2f}")
    print(f"Sell on SushiSwap: ${sell_price:.2f}")
    print(f"Net Profit: ${net_profit:.2f}")

    if net_profit > 0:
        send_slack_message(
            f"💰 *Arbitrage Alert!*\n"
            f"Buy ETH at: ${buy_price:.2f}\n"
            f"Sell ETH at: ${sell_price:.2f}\n"
            f"Net Profit: *${net_profit:.2f}*"
        )
    else:
        print("❌ No profitable opportunity right now.")

simulate_arbitrage()
