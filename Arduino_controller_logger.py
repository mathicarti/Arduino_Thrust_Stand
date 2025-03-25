import serial
import time
import pandas as pd
from library import thrToThrottle, log_data_to_excel

port = "/dev/cu.usbmodem101"
baud_rate = 9600

# Sets up communication with Arduino
ser = serial.Serial(port, baud_rate, timeout=1)

throttle = 0
max_thr = 180
min_thr = 0

sample_time = 5
file_name = ""
trial_name = ""

file_name = f"{input("What is the file name: ")}.xlsx"

print("Calibrating load cell")
time.sleep(1)
print("Done")

while 1:
    thr = input(f"Throttle ({min_thr}, {max_thr}): ")

    if thr == "quit":
        break

    elif thr == "tare":
        ser.write(("tare\n").encode()) # Sends command to tare the cell to the Arduino
        time.sleep(1) # Time for the load cell to tare
        print("Tared load cell")
    
    elif thr.lower() == "log":
        arduino_line = ser.readline().decode().strip() # Gets data from Arduino, and decode it to str
        log_data_to_excel(sample_time, file_name, arduino_line)          

    else:
        throttle = thrToThrottle(thr, throttle)
    
    ser.write((f"{throttle}T\n").encode()) # Sends to the serial aka Arduino

ser.close()