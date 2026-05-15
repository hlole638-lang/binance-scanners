import requests

def run_scan(interval):

    results = []

    symbols = [
        "BTCUSDT",
        "ETHUSDT"
    ]

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

            results.append({

                "symbol": symbol,
                "price": response.text,
                "rsi": 0,
                "score": response.status_code

            })

        except Exception as e:

            results.append({

                "symbol": symbol,
                "price": str(e),
                "rsi": 0,
                "score": 0

            })

    return results
