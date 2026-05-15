from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Scanner Working"

@app.route("/scan/<timeframe>")
def scan(timeframe):

    data = [
        {
            "symbol": "BTCUSDT",
            "price": 103000,
            "rsi": 45,
            "score": 80
        },
        {
            "symbol": "ETHUSDT",
            "price": 2500,
            "rsi": 39,
            "score": 75
        }
    ]

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
