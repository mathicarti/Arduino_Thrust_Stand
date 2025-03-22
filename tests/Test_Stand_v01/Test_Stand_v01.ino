int throttle = 0;

const int loadCellPin = A0;
const int killSwtPin = 2;
const int escPin = 9;

void setup() {
  pinMode(escPin, OUTPUT);
  pinMode(killSwtPin, INPUT_PULLUP);
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  int killSwtVal = digitalRead(killSwtPin);

  if (killSwtVal == LOW) {
    throttle = 0;
  }

  if (Serial.available() > 0) {
    String serialData = Serial.readStringUntil('\n');
    if (serialData.length() > 0) {
      throttle = changeThrottle(serialData);
    }
  }

  analogWrite(escPin, throttle);
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
  Serial.print(throttleVal);
  Serial.print(",");
  Serial.println(loadCellF);

  return 0;
}
