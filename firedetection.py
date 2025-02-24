import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pymongo import MongoClient

# Connexion à la base MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["forestguard"]
collection = db["alerts"]

# Charger les données
data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Vérifier s'il y a des données suffisantes
if df.empty:
    print("Pas de données disponibles.")
else:
    # Sélection des features importantes
    X = df[["temperature", "smoke", "humidity", "soilMoisture"]]
    y = (df["temperature"] > 40) | (df["smoke"] > 700)  # 1 si risque d'incendie

    # Entraînement du modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Faire une nouvelle prédiction
    new_data = np.array([[42, 800, 30, 500]])  # Exemple de nouvelles données
    prediction = model.predict(new_data)

    if prediction[0] == 1:
        print("🔥 Alerte : Risque d'incendie détecté !")

