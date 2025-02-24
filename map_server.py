from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["forestguard"]
collection = db["alerts"]

@app.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = list(collection.find({}, {"_id": 0}))
    return jsonify(alerts)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5001, debug=True)
