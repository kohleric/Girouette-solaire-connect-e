int pinA = 2;   // Le port D2 est associé à l'interruption 0
int pinRPM = 3;
int pinB = 4;
volatile int pos = 0;  // Position (en nombre de pas) du codeur
int posMax = 8;  // 360/16 soit 22.5° de résolution
unsigned long t_avant = 0;
char dir[12];
float rpm = 0.0;

void setup() {
  Serial.begin(115200);
  pinMode(pinB, INPUT);
  pinMode(pinRPM, INPUT);
  attachInterrupt(digitalPinToInterrupt(pinA), front, CHANGE);  // Détection des deux types de fronts
  attachInterrupt(digitalPinToInterrupt(pinRPM), RPM, FALLING);
}

void loop() {
  delay(10); // Assurez-vous que le loop ne s'exécute pas trop rapidement

  // Afficher les dernières valeurs mesurées
  Serial.print("Direction: ");
  Serial.print(dir);
  Serial.print(", Position: ");
  Serial.print(pos);
  Serial.print(", Vitesse angulaire (RPM): ");
  Serial.println(rpm);

  // Vous pouvez également ajouter d'autres opérations de traitement ici
}

void front() {
  int sA = digitalRead(pinA);
  int sB = digitalRead(pinB);

  if (sA == sB) {
    ++pos;
    if (pos == posMax) {
      pos = 0;
    }
  } else {
    --pos;
    if (pos == -1) {
      pos = posMax - 1;
    }
  }
  determineDirection();
}

void determineDirection() {
  switch (pos) {
    case 0: strcpy(dir, "Nord"); break;
    case 1: strcpy(dir, "Nord-Est"); break;
    case 2: strcpy(dir, "Est"); break;
    case 3: strcpy(dir, "Sud-Est"); break;
    case 4: strcpy(dir, "Sud"); break;
    case 5: strcpy(dir, "Sud-Ouest"); break;
    case 6: strcpy(dir, "Ouest"); break;
    case 7: strcpy(dir, "Nord-Ouest"); break;
  }
}

void RPM() {
  unsigned long t_maintenant = millis();
  unsigned long t = t_maintenant - t_avant;
  t_avant = t_maintenant;

  rpm = 60000.0 / (t * 2.0);
}