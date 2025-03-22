import serial
import time
import pandas as pd

port = "/dev/cu.usbmodem101"
baud_rate = 9600

# Sets up communication with Arduino
ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(1)

time_init = time.time()
sample_time = 30
logging = 1
throttle = ""
weight = ""

df = pd.DataFrame(columns=["Time", "Throttle", "Weight"]) # Sets the "boilerplate" for the data table

while logging: # Takes the first 10 values for convenience 
    time_current = time.time()

    try:
        arduino_line = ser.readline().decode().strip() # Gets data from Arduino, and decode it to str
        throttle, weight = arduino_line.split(",") # Parses data from Arduino into throttle and weight

    except:
        pass # In case of bad formatted data or any error

    try:
        new_row = pd.DataFrame({"Time": [time_current - time_init], "Throttle": [int(throttle)], "Weight": [int(weight)]}) # Gets all the data and formats it into a new data row
        df = pd.concat([df, new_row], ignore_index=True) # Inserts the new row at the end of the main data table
        df.to_excel("test_data.xlsx", sheet_name="New Sheet", index=False) # Save the processed data (time, throttle, weight) to excel file and removes the index count

    except:
        pass

    if (sample_time - (time_current - time_init)) < 0: # Stops logging when hits the time limit
        logging = 0

ser.close()
