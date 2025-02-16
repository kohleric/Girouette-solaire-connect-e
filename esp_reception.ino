// Programme pour le récepteur (ESP32)

// Inclure la bibliothèque pour la communication série
#include <HardwareSerial.h>

// Configuration de la broche de réception
const int esp32RxPin = 34; // Broche RX de l'ESP32

void setup() {
  // Initialisation de la communication série avec la vitesse de transmission 9600 bps
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, esp32RxPin, -1); // Configurer Serial1 avec RX sur la broche 34
}

void loop() {
  // Lire les données de l'Arduino Nano et les afficher sur le moniteur série de l'ESP32
  while (Serial1.available()) {
    char c = Serial1.read();
    Serial.print(c);
  }

}