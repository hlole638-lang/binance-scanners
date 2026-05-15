import requests

def run_scan(interval):

    symbols = [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "XRPUSDT"
    ]

    results = []

    for symbol in symbols:

        try:

            url = (
                "https://api.binance.com/api/v3/ticker/price"
                f"?symbol={symbol}"
            )

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            price = float(data["price"])

            results.append({

                "symbol": symbol,
                "price": round(price, 4),
                "rsi": 50,
                "score": 80

            })

        except Exception as e:

            print(symbol, e)

    return results
