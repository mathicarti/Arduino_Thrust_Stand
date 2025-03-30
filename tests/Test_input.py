import serial
import time
import pandas as pd
import library

port = "/dev/cu.usbmodem101"
baud_rate = 9600

# Sets up communication with Arduino
ser = serial.Serial(port, baud_rate, timeout=1)

print("Calibrating load cell")
time.sleep(1)
print("Done")

df = 

while 1:
    log_input = input("WHAT!: ")

    if log_input == "q":
        break

    elif log_input.isnumeric():
        arduino_line = ser.readline().decode().strip()

        print(f"Sampling data for {log_input} seconds")

        index_count = 0
        time_init = time.time()
        logging = True

        df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": []}) # Boilerplate for table

        while logging:
            time_current = time.time()

            try:
                weight, throttle = arduino_line.split(",") # Parses data from Arduino into throttle and weight

                print(weight, throttle)

                new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)]}) # Gets all the data and formats it into a new data row
                df = pd.concat([df, new_row], ignore_index=True)
                print(df)

            except Exception as e:
                print(e)
                pass

            if (log_input - (time_current - time_init)) < 0: # Stops logging when hits the time limit
                logging = False 
