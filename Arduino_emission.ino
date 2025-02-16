void setup() {
  // Initialisation de la communication série avec la vitesse de transmission 9600 bps
  Serial.begin(115200);

  // Initialisation de la communication série sur la broche TX
  //Serial1.begin(9600);
}

void loop() {
  // Envoyer des données à l'ESP32 via la broche TX
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0) * 2;
  Serial.print("Hello from Arduino Nano!");Serial.print(",");Serial.println(voltage); // Utilisation de Serial1 pour la broche TX
  //Serial.println("message envoyé!");
  delay(1000); // Attente d'une seconde avant d'envoyer la prochaine donnée
}