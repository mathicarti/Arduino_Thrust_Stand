#include <Servo.h>

Servo ESC;

int speed;

const int ESC_PIN = 9;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ESC.attach(escPin,1000,2000);
  delay(1);
  ESC.write(10);
  delay(5000);
  Serial.setTimeout(10);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String serialData = Serial.readStringUntil('\n');
    speed = 
  }
  speed = map(speed, 0, 1023, 0, 180);
  ESC.write(speed);
}
