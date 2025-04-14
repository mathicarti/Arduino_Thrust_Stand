#include <HX711_ADC.h>
#include <EEPROM.h>
#include <Servo.h>

// Necessary pins on Arduino and variables
const int loadCellPin = A0;
const int escPin = 9;
const int HX711_dout = 4;
const int HX711_sck = 5;

int throttle = 0;

const int calVal_eepromAdress = 0;
unsigned long t = 0;

// Initialise load cell and ESC
Servo ESC;
HX711_ADC LoadCell(HX711_dout, HX711_sck);

void setup() {
  // "Arms" the ESC
  Serial.begin(9600);
  delay(5000);
  ESC.attach(escPin,1000,2000);
  delay(1);
  ESC.write(10);
  delay(5000);

  // Calibration of the load cell
  LoadCell.begin();
  Serial.println();
  Serial.println("Calibrating Cell");

  float calibrationValue; // Can recalibrate with Calibration.ino
  calibrationValue = 696.0;

  EEPROM.get(calVal_eepromAdress, calibrationValue); // Gets saved calibration value from EEPROM

  unsigned long stabilizingtime = 3000; // Time needed to get baseline weight
  
  boolean _tare = true;
  LoadCell.start(stabilizingtime, _tare);
  
  if (LoadCell.getTareTimeoutFlag()) { // If any bad connection detected
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  } else {
    LoadCell.setCalFactor(calibrationValue); // Set calibration value
    Serial.println("Startup is complete");
  }

  Serial.setTimeout(10);
}

void loop() {
  static boolean newDataReady = 0;
  
  if (Serial.available() > 0) { // Gets any inputs from Serial, and checks if its a throttle. If 't' sent, load cell tared (set to 0g)
    String serialData = Serial.readStringUntil('\n');
    throttle = changeThrottle(serialData);
    tare_cell(serialData);
  }

  ESC.write(throttle); // Sends the throttle to the ESC

  if (LoadCell.update() == 1) { // if any new weight data, send out weight and throttle values
    float weight = LoadCell.getData();
    readVal(throttle, weight);
    newDataReady = 0;
    t = millis();
  }

  delay(10);
}

int changeThrottle(String serThr) { // Sets the new throttle (between 0-180) sent through Serial (e.g. "103T") and returns it
  int thr = 0;

  if (serThr.endsWith("T")) {
    serThr.remove(serThr.indexOf("T"), 1);
    thr = serThr.toInt();
  } else {
    thr = throttle;
  }

  return thr;
}
void tare_cell(String serTare) { 
  if (serTare == "tare") { 
    LoadCell.tareNoDelay();
  } 
}

void readVal(int throttleVal, float loadCellF) { // Parses output and sends it through Serial
  Serial.print(loadCellF, 5);
  Serial.print(",");
  Serial.println(throttleVal);

  return 0;
}
