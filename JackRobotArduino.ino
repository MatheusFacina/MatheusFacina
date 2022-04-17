#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Wire.h>

//Define a bussola
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

#include <math.h>

#include <Servo.h>

// Motor left
const int dir1PinA = 7;
const int dir2PinA = 8;
const int speedPinA = 5; // control motor speed

// Motor right
const int dir1PinB = 12;
const int dir2PinB = 13;
const int speedPinB = 6; 

// Sonar front
const int fsEchoPin = 3;
const int fsTriggerPin = 4;

// Sonar left
const int lsEchoPin = 9;
const int lsTriggerPin = 10;

// Sonar right
const int rsEchoPin = 1;
const int rsTriggerPin = 2;

// Servo motor
const int servoPin = 11;

Servo servo;

void setup(){    
  pinMode(dir1PinA,OUTPUT);
  pinMode(dir2PinA,OUTPUT);
  pinMode(speedPinA,OUTPUT);
  pinMode(dir1PinB,OUTPUT);
  pinMode(dir2PinB,OUTPUT);
  pinMode(speedPinB,OUTPUT);
  pinMode(fsTriggerPin, OUTPUT);
  pinMode(lsTriggerPin, OUTPUT);
  pinMode(rsTriggerPin, OUTPUT);
  pinMode(fsEchoPin, INPUT);
  pinMode(lsEchoPin, INPUT);
  pinMode(rsEchoPin, INPUT);
  servo.attach(servoPin);
}

void loop(){
  vaievolta();
}

float getMag(){
   
  sensors_event_t event; 
  mag.getEvent(&event);

  //Arctangente de x e y
  float heading = atan2(event.magnetic.y, event.magnetic.x);
  
  // Corrige se o sinal estiver reverso.
  if(heading < 0)
    heading += 2*PI;
   
  // Convertendo para graus
  float headingDegrees = heading * 57.2957795131; 
  return headingDegrees;
}

long hearSonar (int sonar){
  int i;
  long aux;
  int anterior , atual;
  long soma=0;
  int triggerPin , echoPin; 
  long durations[5];
  long duration;
  switch (sonar){
    case 0:
      triggerPin = lsTriggerPin;
      echoPin = lsEchoPin;
      break;     
    case 1:
      triggerPin = fsTriggerPin;
      echoPin = fsEchoPin;
      break;
    case 2:
      triggerPin = rsTriggerPin;
      echoPin = rsEchoPin;
      break;
    default:
      return -1;
  }
  
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(triggerPin, LOW);
  durations[0] = pulseIn(echoPin, HIGH);
  
  for(i=1;i<5;i++){
        digitalWrite(triggerPin, LOW);
        delayMicroseconds(2);
        digitalWrite(triggerPin, HIGH);
        delayMicroseconds(5);
        digitalWrite(triggerPin, LOW);
        durations[i] = pulseIn(echoPin, HIGH);
        atual = i;
        anterior = i-1;
        while(anterior >= 0 && durations[atual] < durations[anterior]){
          aux = durations[atual];
          durations[atual] = durations[anterior];
          durations[anterior] = aux;
          atual = atual-1;
          anterior = anterior-1;
          }
          
  }
  soma = durations[1] + durations[2] + durations[3];
  duration = soma / 3;
  return duration / 29 / 2;
}

// Motor Control Function
void motorCtrl (int action){
  switch (action){
    case 0: // Parar motores
      // Right Motor
      analogWrite(speedPinA, 0);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      // Left Motor
      analogWrite(speedPinB, 0);
      digitalWrite(dir1PinB, LOW);
      digitalWrite(dir2PinB, HIGH);
      break;
    case 1: // Fazer curva para esquerda
      //Right Motor
      analogWrite(speedPinA, 255);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      // Left Motor
      analogWrite(speedPinB, 255);
      digitalWrite(dir1PinB, HIGH);
      digitalWrite(dir2PinB, LOW);
      break;
    case 2: // Andar para frente
      //Right Motor
      analogWrite(speedPinA, 255);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      // Left Motor
      analogWrite(speedPinB, 255);
      digitalWrite(dir1PinB, LOW);
      digitalWrite(dir2PinB, HIGH);
      break;
    case 3: // Curva para direita
      //Right Motor
      analogWrite(speedPinA, 255);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      // Left Motor
      analogWrite(speedPinB, 255);
      digitalWrite(dir1PinB, HIGH);
      digitalWrite(dir2PinB, LOW);
      break;
    case 4: // Andar para Tras
      //Right Motor
      analogWrite(speedPinA, 255);
      digitalWrite(dir1PinA, HIGH);
      digitalWrite(dir2PinA, LOW);
      // Left Motor
      analogWrite(speedPinB, 255);
      digitalWrite(dir1PinB, HIGH);
      digitalWrite(dir2PinB, LOW);
      break;
    default:
      // Right Motor
      analogWrite(speedPinA, 0);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      // Left Motor
      analogWrite(speedPinB, 0);
      digitalWrite(dir1PinB, LOW);
      digitalWrite(dir2PinB, HIGH);
  
  }

}


void servoCntrl(int action){ //Controle Do Servo
  switch (action){
    case 0: //Servo a 0°
      servo.write(0);
      delay(800);
      break;
    case 1: //Servo a 45°
      servo.write(45);
      delay(800);
      break;
    case 2: //Servo a 90°
      servo.write(90);
      delay(800);
      break;
    case 3: //Servo a 135°
      servo.write(135);
      delay(800);
      break;
    case 4: //Servo a 180°
      servo.write(180);
      delay(800);
      break;
  }

}


void vaievolta(){ //Função que faz o servo ir e voltar
  int i;
 
  for(i = 1 ; i <= 4 ; i++)
    servoCntrl(i);
    
  for(i = 3 ; i >= 0 ; i--) 
    servoCntrl(i);

}

