#include <HX711_ADC.h>
#include <EEPROM.h>

//pins:
const int HX711_dout = 4;
const int HX711_sck = 5;

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

void setup() {
  Serial.begin(57600); delay(10);
  LoadCell.begin();
  Serial.println();
  Serial.println("Calibrating Cell");

  float calibrationValue; // Can recalibrate with Calibration.ino
  calibrationValue = 696.0;

  EEPROM.get(calVal_eepromAdress, calibrationValue); // Gets saved calibration value from EEPROM

  unsigned long stabilizingtime = 3000; // time needed to get baseline weight
  
  boolean _tare = true;
  LoadCell.start(stabilizingtime, _tare);
  
  if (LoadCell.getTareTimeoutFlag()) { // if any bad connection detected
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue); // set calibration value
    Serial.println("Startup is complete");
  }
}

void loop() {
  static boolean newDataReady = 0;

  // check for new data/start next conversion and prints it
  if (LoadCell.update() == 1) {
    float weight = LoadCell.getData();
      Serial.println(weight);
      newDataReady = 0;
      t = millis();
  }

  // if 't' sent, load cell tared
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay();
  }
}
