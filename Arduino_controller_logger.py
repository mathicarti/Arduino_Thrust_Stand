import serial
import time
import pandas as pd

port = "/dev/cu.usbmodem101"
baud_rate = 9600

# Sets up communication with Arduino
ser = serial.Serial(port, baud_rate, timeout=1)

throttle = 0
max_thr = 180
min_thr = 0

time_init = time.time()
sample_time = 20
logging = True
throttle = ""
weight = ""

file_name = ""
trial_name = ""

def parseThr(thrInputCommand): # Parses throttle input into command (+, -, exact) and value (add, sub, exact)
    command = ""
    value = 0

    if thrInputCommand.startswith("+"):
        command = "+"
        if thrInputCommand.replace("+", "") != "":
            value = int(thrInputCommand.replace("+", ""))
        else:
            value = 1

    elif thrInputCommand.startswith("-"):
        command = "-"
        if thrInputCommand.replace("-", "") != "":
            value = int(thrInputCommand.replace("-", ""))
        else:
            value = 1

    elif thrInputCommand.isnumeric():
        command = ""
        value = int(thrInputCommand)

    else:
        command = "TERMINATE"
        value = 0
    
    return command, value

def thrToThrottle(thrInput, realThrottle): # Handles making the new throttle, parses the input then add/sub or exact (with max and min ceilings) to throttle
    futureThr = 0
    thrCommand, thrValue = parseThr(thrInput)

    if thrCommand == "+":
        futureThr = min((realThrottle+thrValue), max_thr)

    elif thrCommand == "-":
        futureThr = max((realThrottle-thrValue), min_thr)

    elif thrCommand == "":
        if thrValue >= min_thr and thrValue <= max_thr:
            futureThr = thrValue
        else:
            futureThr = realThrottle

    elif thrCommand == "TERMINATE":
        futureThr = 0
        print("ESC STOPPED")

    else:
        futureThr = realThrottle
    
    print(f"Throttle set to: {throttle}")

    return futureThr

file_name = f"{input("What is the file name: ")}.xlsx"

print("Calibrating load cell")
time.sleep(3)
print("Done")

while 1:
    thr = input(f"Throttle ({min_thr}, {max_thr}): ")

    if thr == "quit":
        break

    elif thr == "tare":
        ser.write(("tare\n").encode()) # Sends command to tare the cell to the Arduino
        time.sleep(3) # Time for the load cell to tare
        print("Tared load cell")
    
    elif thr.lower() == "log":
        radius = input("What is the radius of the propeller: ")
        angle = input("What is the blade angle: ")
        rpm = input("what is the RPM: ")
        trial = input("What is the trial number (1-5): ")
        trial_name = f"{radius}mm_{angle}deg_{rpm}RPM_{trial}"

        logging = True

        print(f"Recording for {sample_time} milliseconds, on file {file_name}, on sheet {trial_name}")

        index_count = 0

        while logging:
            time_current = time.time()

            df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": [], "Average": []}) # Boilerplate for sheet

            try:
                arduino_line = ser.readline().decode().strip() # Gets data from Arduino, and decode it to str
                throttle, weight = arduino_line.split(",") # Parses data from Arduino into throttle and weight

                index_count += 1
                if index_count == 1:
                    new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": ["=AVERAGE(C$2:C$10000)"]}) # New first row, with average calculation
                else:
                    new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": [""]}) # Gets all the data and formats it into a new data row
                df = pd.concat([df, new_row], ignore_index=True) # Inserts the new row at the end of the main data table

                with pd.ExcelWriter(file_name, mode="a", if_sheet_exists="replace") as writer: # Save the processed data (time, throttle, weight) to excel file and removes the index count
                    df.to_excel(writer, sheet_name=trial_name, index=False)
                print("logged")

            except Exception as e:
                print(e)
                pass # In case of bad formatted data or any error

            if (sample_time - (time_current - time_init)) < 0: # Stops logging when hits the time limit
                logging = False               

    else:
        throttle = thrToThrottle(thr, throttle)
    
    ser.write((f"{throttle}T\n").encode()) # Sends to the serial aka Arduino

ser.close()