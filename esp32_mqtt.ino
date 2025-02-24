#include <PubSubClient.h>
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  client.setServer("broker.hivemq.com", 1883); // Utilisation d’un broker public
}

void loop() {
  if (!client.connected()) {
    client.connect("ESP32Client");
  }

  String payload = "{\"temperature\": " + String(temp) + ", \"smoke\": " + String(smokeLevel) + "}";
  client.publish("forestguard/alerts", payload.c_str());
  delay(5000);
}
