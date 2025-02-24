from flask import Flask, request, jsonify
from pymongo import MongoClient
from twilio.rest import Client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
load_dotenv()

app = Flask(__name__)

# Connexion MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["forestguard"]
collection = db["alerts"]
collection.create_index([("temperature", 1)])

# Twilio Configuration
TWILIO_SID = "VOTRE_SID"
TWILIO_TOKEN = "VOTRE_TOKEN"
TWILIO_PHONE = "VOTRE_NUMERO_TWILIO"
TO_PHONE = "+212XXXXXXXXX"  # Numéro de l'alerte

def send_sms_alert(message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(body=message, from_=TWILIO_PHONE, to=TO_PHONE)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    print("Données reçues:", data)

    # Stocker dans la base de données
    collection.insert_one(data)

    # Détection d'alerte
    if data["temperature"] > 40 or data["smoke"] > 700:
        alert_msg = f"🔥 Alerte incendie ! {data['temperature']}°C, Fumée: {data['smoke']}. Coordonnées: {data['latitude']}, {data['longitude']}"
        send_sms_alert(alert_msg)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)