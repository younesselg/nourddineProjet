#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

// Définition des broches des capteurs
#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ2PIN 34
#define SOIL_MOISTURE_PIN 35
#define BUZZER_PIN 32

// Initialisation des capteurs
DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

// Connexion WiFi
const char* ssid = "VOTRE_SSID";
const char* password = "VOTRE_MOT_DE_PASSE";
const char* serverUrl = "http://votre-serveur.com/data";

void setup() {
    Serial.begin(115200);
    dht.begin();
    pinMode(MQ2PIN, INPUT);
    pinMode(SOIL_MOISTURE_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    gpsSerial.begin(9600, SERIAL_8N1, 16, 17);
    
    // Connexion WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connexion WiFi en cours...");
    }
    Serial.println("Connecté au WiFi");
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int smokeLevel = analogRead(MQ2PIN);
    int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
    double latitude = 0.0, longitude = 0.0;

    if (gpsSerial.available()) {
        gps.encode(gpsSerial.read());
        if (gps.location.isUpdated()) {
            latitude = gps.location.lat();
            longitude = gps.location.lng();
        }
    }
    
    Serial.printf("Température: %.2f°C | Humidité: %.2f%% | Fumée: %d | Humidité sol: %d\n", 
                  temperature, humidity, smokeLevel, soilMoisture);

    // Détection de risque d'incendie
    if (temperature > 40 || smokeLevel > 700) {
        Serial.println("🔥 Risque d'incendie détecté ! Alerte envoyée. 🚨");
        digitalWrite(BUZZER_PIN, HIGH);
        sendAlert(temperature, humidity, smokeLevel, soilMoisture, latitude, longitude);
        delay(5000);
        digitalWrite(BUZZER_PIN, LOW);
    }
    delay(2000);
}

void sendAlert(float temp, float hum, int smoke, int soil, double lat, double lon) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");
        
        String jsonPayload = "{";
        jsonPayload += "\"temperature\":" + String(temp) + ",";
        jsonPayload += "\"humidity\":" + String(hum) + ",";
        jsonPayload += "\"smoke\":" + String(smoke) + ",";
        jsonPayload += "\"soilMoisture\":" + String(soil) + ",";
        jsonPayload += "\"latitude\":" + String(lat, 6) + ",";
        jsonPayload += "\"longitude\":" + String(lon, 6) + "}";
        
        int httpResponseCode = http.POST(jsonPayload);
        if (httpResponseCode > 0) {
            Serial.printf("Réponse du serveur: %d\n", httpResponseCode);
        } else {
            Serial.println("Erreur d'envoi des données");
        }
        http.end();
    }
}
