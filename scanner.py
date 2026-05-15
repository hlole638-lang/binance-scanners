import requests

def run_scan(interval):

    symbols = [
        "BTC-USDT",
        "ETH-USDT",
        "BNB-USDT",
        "SOL-USDT",
        "XRP-USDT"
    ]

    results = []

    for symbol in symbols:

        try:

            url = (
                "https://api.kucoin.com/api/v1/market/orderbook/level1"
                f"?symbol={symbol}"
            )

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            price = float(
                data["data"]["price"]
            )

            results.append({

                "symbol": symbol,
                "price": round(price, 4),
                "rsi": 50,
                "score": 80

            })

        except Exception as e:

            results.append({

                "symbol": symbol,
                "price": str(e),
                "rsi": 0,
                "score": 0

            })

    return results
