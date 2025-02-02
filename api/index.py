import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_URL = "https://tele-tool.vercel.app/ff?id="

@app.route("/pybotz", methods=["GET"])
def fetch_data():
    item_id = request.args.get("id")
    if not item_id:
        return jsonify({"error": "id parameter is required"}), 400
    try:
        response = requests.get(API_URL + item_id)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from the external API"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run()
