#include "HX711.h"

HX711 myScale;

int const cell_data_PIN = 4;
int const cell_clock_PIN = 6;

myScale.set_offset(68289);
myScale.set_scale(1071.572875);


void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
