from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "simulated_trades.csv"

# Create CSV if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "symbol", "side", "price"])

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        side = data.get("side")
        price = data.get("price")

        if not all([symbol, side, price]):
            return jsonify({"error": "Missing required fields"}), 400

        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.utcnow().isoformat(), symbol, side, price])

        return jsonify({"message": "Simulated trade logged"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
