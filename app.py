from flask import Flask, jsonify, render_template
from scanner import run_scan

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/scan/<timeframe>")
def scan(timeframe):

    data = run_scan(timeframe)

    return jsonify(data)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=3000)
