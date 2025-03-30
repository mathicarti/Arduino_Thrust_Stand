import serial
import time
import pandas as pd

throttle = 0
max_thr = 180
min_thr = 0

sample_time = 5
file_name = ""

class SerialHandler:
    def __init__(self, ard_port="/dev/cu.usbmodem101", baud_rate=9600, time_out=1):
        self.ser = serial.Serial(port=ard_port, baudrate=baud_rate, timeout=time_out)
        print("Calibrating load cell")
        time.sleep(1)
        print("Done")

    def send(self, message):
        self.ser.write((f"{message}\n").encode())

    def receive(self):
        return self.ser.readline().decode().strip()
    
    def close(self):
        self.ser.close()

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
    
    print(f"Throttle set to: {futureThr}")

    thrMessage = f"{futureThr}T"
    sh.send(thrMessage)

def tare():
    sh.send("tare") # Sends command to tare the cell to the Arduino
    time.sleep(1) # Time for the load cell to tare
    print("Tared load cell")

def log_data_to_excel(logging_time, logging_file_name):
    radius = input("What is the radius of the propeller: ")
    angle = input("What is the blade angle: ")
    rpm = input("what is the RPM: ")
    trial = input("What is the trial number (1-5): ")
    trial_name = f"{radius}mm_{angle}deg_{rpm}RPM_{trial}"

    print(f"Recording for {logging_time} milliseconds, on file {logging_file_name}, on sheet {trial_name}")

    index_count = 0
    time_init = time.time()
    logging = True

    df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": [], "Average": []}) # Boilerplate for sheet

    while logging:
        time_current = time.time()
        
        try:
            arduino_line = sh.receive() # Gets data from Arduino, and decode it to str
            weight, throttle = arduino_line.split(",") # Parses data from Arduino into throttle and weight
            
            index_count += 1
            
            if index_count == 1:
                new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": ["=AVERAGE(B$2:B$10000)"]}) # New first row, with average calculation
            
            else:
                new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": [""]}) # Gets all the data and formats it into a new data row
            
            df = pd.concat([df, new_row], ignore_index=True) # Inserts the new row at the end of the main data table

            with pd.ExcelWriter(logging_file_name, mode="a", if_sheet_exists="replace") as writer: # Save the processed data (time, throttle, weight) to excel file and removes the index count
                df.to_excel(writer, sheet_name=trial_name, index=False)

            print(df)

        except Exception as e:
            print(e)
            pass # In case of bad formatted data or any error

        if (logging_time - (time_current - time_init)) < 0: # Stops logging when hits the time limit
            logging = False 

def quick_log(logging_time=2):
    print(f"Sampling data for {logging_time} seconds")

    time_init = time.time()
    logging = True

    df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": []}) # Boilerplate for table

    while logging:
        time_current = time.time()

        try:
            arduino_line = sh.receive() # Gets data from Arduino, and decode it to str
            print(arduino_line)
            weight, throttle = arduino_line.split(",") # Parses data from Arduino into throttle and weight

            new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)]}) # Gets all the data and formats it into a new data row
            df = pd.concat([df, new_row], ignore_index=True)
            print(df)

        except Exception as e:
            print(e)
            pass

        if (logging_time - (time_current - time_init)) < 0: # Stops logging when hits the time limit
            logging = False 

sh = SerialHandler()