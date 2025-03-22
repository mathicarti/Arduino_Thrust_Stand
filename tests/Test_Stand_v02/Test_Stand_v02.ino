#include <Servo.h>

Servo ESC;

int throttle = 0;

const int loadCellPin = A0;
const int escPin = 9;

void setup() {
  Serial.begin(9600);
  ESC.attach(escPin,1000,2000);
  delay(1);
  ESC.write(10);
  delay(5000);
  Serial.setTimeout(10);
}

void loop() {
  if (Serial.available()) {
    String serialData = Serial.readStringUntil('\n');
    throttle = changeThrottle(serialData);
  }

  ESC.write(throttle);
  readVal(throttle, analogRead(loadCellPin));
  delay(10);
}

int changeThrottle(String serThr) {
  int thr = 0;

  if (serThr.endsWith("T")) {
    serThr.remove(serThr.indexOf("T"), 1);
    thr = serThr.toInt();
  } else {
    thr = throttle;
  }

  return thr;
}

void readVal(int throttleVal, int loadCellF) {
  Serial.print(loadCellF);
  Serial.print(",");
  Serial.println(throttleVal);

  return 0;
}
