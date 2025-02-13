from flask import Flask, request, jsonify
from pymongo import MongoClient
from twilio.rest import Client

app = Flask(__name__)

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["forestguard"]
collection = db["alerts"]

# Twilio Configuration
TWILIO_SID = "VOTRE_SID"
TWILIO_TOKEN = "VOTRE_TOKEN"
TWILIO_PHONE = "VOTRE_NUMERO_TWILIO"
TO_PHONE = "+212XXXXXXXXX"  # Numéro de l'alerte

def send_sms_alert(message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(body=message, from_=TWILIO_PHONE, to=TO_PHONE)

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
