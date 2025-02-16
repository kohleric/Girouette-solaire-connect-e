 #include <WiFi.h>

const char* ssid = "E8C6_2.4";
const char* password = "crapouillot";

const char* odroidIP = "192.168.1.17";
const int odroidPort = 1234;

void setup() {
  Serial.begin(115200);

  // Se connecter au réseau WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au WiFi...");
  }
  Serial.println("Connecté au WiFi");

  delay(1000);
}

void loop() {
  // Envoyer des données à l'Odroid
  // Assurez-vous d'adapter cette partie selon le format de vos données
  String dataToSend = "Donnees_a_envoyer";
  sendDataToOdroid(dataToSend);

  delay(5000); // Envoyer les données toutes les 5 secondes (ajustez selon vos besoins)
}

void sendDataToOdroid(String data) {
  WiFiClient client;

  if (client.connect(odroidIP, odroidPort)) {
    Serial.println("Connexion à l'Odroid établie");
    client.print(data);
    client.stop();
  } else {
    Serial.println("Impossible de se connecter à l'Odroid");
  }
}
