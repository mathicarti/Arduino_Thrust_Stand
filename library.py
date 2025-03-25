import time
import pandas as pd

throttle = 0
max_thr = 180
min_thr = 0

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

def log_data_to_excel(logging_time, logging_file_name, arduino_output_line):
    radius = input("What is the radius of the propeller: ")
    angle = input("What is the blade angle: ")
    rpm = input("what is the RPM: ")
    trial = input("What is the trial number (1-5): ")
    trial_name = f"{radius}mm_{angle}deg_{rpm}RPM_{trial}"

    logging = True

    print(f"Recording for {logging_time} milliseconds, on file {logging_file_name}, on sheet {trial_name}")

    index_count = 0
    time_init = time.time()
    logging = True

    df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": [], "Average": []}) # Boilerplate for sheet

    while logging:
        time_current = time.time()

        try:
            weight, throttle = arduino_output_line.split(",") # Parses data from Arduino into throttle and weight
            index_count += 1

            print(throttle, weight)
            
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