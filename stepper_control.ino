/** Interfacing Python with Stepper Motor Control **/
//Nema 17 Steps per revolution = 200

//defines pin numbers
const int stepPin = 3; //has pulse-width-modulation
const int dirPin = 4; 
int inputSteps = 0; //for incoming serial data

void setup() {
  //Sets the two pins as outputs
  pinMode(stepPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
  //only change motor functions if new data input 
  while (Serial.available() > 0){
    inputSteps = Serial.parseInt();

    Serial.write(inputSteps);

    digitalWrite(dirPin, HIGH);
    for(int x = 0; x < inputSteps; x++) {
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(500); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(500); 
    }
  }
}
