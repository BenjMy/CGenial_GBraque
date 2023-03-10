Voici un protocole détaillé pour montrer aux élèves comment utiliser une carte Arduino connectée à un capteur d'ultrasons pour détecter un objet:

Matériaux nécessaires:

Carte Arduino Uno
Capteur d'ultrasons HC-SR04
LED
Résistance de 220 ohms
Fils de raccordement
Objet à détecter
Étape 1: Branchement du capteur d'ultrasons

Connectez le pin VCC du capteur à la broche 5V de la carte Arduino
Connectez le pin GND du capteur à la broche GND de la carte Arduino
Connectez le pin Trig du capteur à la broche numérique 12 de la carte Arduino
Connectez le pin Echo du capteur à la broche numérique 11 de la carte Arduino
Étape 2: Ajout de la LED

Placez une résistance de 220 ohms entre la broche 9 de la carte Arduino et l'anode de la LED (broche longue)
Connectez la cathode de la LED (broche courte) à la broche GND de la carte Arduino
Étape 3: Programmation de la carte Arduino

Ouvrez le logiciel Arduino IDE sur l'ordinateur
Copiez et collez le code suivant dans l'éditeur de code:


```arduino
const int trigPin = 12;
const int echoPin = 11;
const int ledPin = 9;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  if (distance < 10) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
  Serial.print(distance);
  Serial.println(" cm");
  delay(500);
}
``` 

Téléversez le code sur la carte Arduino en cliquant sur l'icône "Téléverser" dans le menu supérieur.
Étape 4: Test du capteur d'ultrasons

Ouvrez le moniteur série en cliquant sur l'icône "Moniteur série" dans le menu supérieur.
Réglez la vitesse de transmission en bauds sur 9600.
Placez l'objet à détecter devant le capteur d'ultrasons.
Le moniteur série affichera la distance entre le capteur et l'objet en centimètres. Si la distance est inférieure à 10 cm, la LED s'allume.
Note: Pour adapter ce code à l'expérience de chasse au trésor, vous pouvez modifier la distance de détection en fonction de la position de l'objet caché dans la boîte.



Pour moduler la distance de détection facilement avec un bouton, vous pouvez ajouter un potentiomètre à votre circuit et utiliser sa valeur pour régler la distance de détection. Voici comment procéder :

Connectez le potentiomètre à la carte Arduino :

Connectez la broche gauche (ou la broche centrale si elle est marquée) à la broche 5V de la carte Arduino
Connectez la broche droite à la broche GND de la carte Arduino
Connectez la broche centrale (ou la broche gauche si elle n'est pas marquée) à une broche analogique de la carte Arduino, par exemple la broche A0.
Modifiez le code pour utiliser la valeur du potentiomètre comme distance de détection :

Dans la fonction setup(), ajoutez la ligne suivante pour initialiser le potentiomètre : pinMode(A0, INPUT);
Dans la fonction loop(), ajoutez la ligne suivante pour lire la valeur du potentiomètre : int threshold = map(analogRead(A0), 0, 1023, 2, 200);
Remplacez la valeur fixe "10" dans la condition if (distance < 10) par la variable threshold.
Le potentiomètre vous permettra de régler la distance de détection en faisant varier la tension sur la broche A0 de la carte Arduino. Vous pouvez utiliser la fonction map() pour convertir la valeur lue sur le potentiomètre (entre 0 et 1023) en une distance de détection en cm. Par exemple, si vous voulez que la distance de détection varie entre 2 cm et 200 cm, vous pouvez utiliser la ligne de code ci-dessus pour convertir la valeur lue sur le potentiomètre en une valeur entre 2 et 200.


Dealing with multiple echoes can be a common problem when using ultrasonic sensors such as the HC-SR04. This can happen when the ultrasonic waves bounce off of multiple objects and return to the sensor at different times, leading to erroneous distance measurements.

One way to deal with multiple echoes is to use a technique called pulse width filtering. This involves measuring the duration of the ultrasonic pulse and ignoring any subsequent pulses that arrive within a certain time window after the initial pulse. This can help to filter out any secondary echoes that may be detected.

Here is an example Arduino code that implements pulse width filtering for the HC-SR04 sensor:

```arduino
#define trigPin 9
#define echoPin 10
#define pulseWidth 10 // time window for pulse width filtering, in microseconds

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  unsigned long duration = pulseIn(echoPin, HIGH);
  
  if (duration > 0 && duration < pulseWidth * 2) {
    // valid pulse detected
    float distance = duration / 58.0; // convert pulse duration to distance in cm
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
  }
  
  delay(100);
}
``` 
