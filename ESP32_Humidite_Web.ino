#include <WiFi.h>
#include <WebServer.h>
#include <FS.h>
#include <SPIFFS.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Ton_SSID";
const char* password = "Ton_MotDePasse";

WebServer server(80);

void handleRoot() {
  File file = SPIFFS.open("/index.html", "r");
  if (!file) {
    server.send(404, "text/plain", "Fichier introuvable");
    return;
  }
  server.streamFile(file, "text/html");
  file.close();
}

void handleData() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  String json = "{\"temperature\":" + String(t) + ",\"humidity\":" + String(h) + "}";
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  if (!SPIFFS.begin(true)) {
    Serial.println("Erreur SPIFFS");
    return;
  }

  WiFi.begin(ssid, password);
  Serial.print("Connexion Wi-Fi en cours");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté !");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.begin();
  Serial.println("Serveur web démarré !");
}

void loop() {
  server.handleClient();
}
