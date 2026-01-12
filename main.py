import requests
import csv
import time
from datetime import datetime

API_URL = "https://gamma-api.polymarket.com/markets"
LOG_FILE = "polymarket_prices.csv"
INTERVAL_SECONDS = 60  # 1 minute


def fetch_markets():
    params = {
        "active": "true",
        "limit": 50
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()

    # IMPORTANT: API returns a LIST, not a dict
    return response.json()


def init_csv():
    try:
        with open(LOG_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "market_id",
                "question",
                "outcome",
                "price"
            ])
    except FileExistsError:
        pass


def log_prices(markets):
    timestamp = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for market in markets:
            market_id = market.get("id")
            question = market.get("question")

            outcomes = market.get("outcomes", [])
            prices = market.get("outcomePrices", [])

            if not outcomes or not prices:
                continue

            for outcome, price in zip(outcomes, prices):
                writer.writerow([
                    timestamp,
                    market_id,
                    question,
                    outcome,
                    price
                ])


def main():
    init_csv()
    print("Starting Polymarket price logger...")

    while True:
        try:
            markets = fetch_markets()
            log_prices(markets)
            print(f"Logged {len(markets)} markets at {datetime.utcnow().isoformat()} UTC")
        except Exception as e:
            print("Error:", e)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
