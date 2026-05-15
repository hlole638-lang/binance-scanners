from flask import Flask, render_template, jsonify
from scanner import run_scan

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan/<timeframe>")
def scan(timeframe):
    results = run_scan(timeframe)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
