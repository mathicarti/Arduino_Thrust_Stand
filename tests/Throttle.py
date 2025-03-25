import time
import pandas as pd

throttle = 0
max_thr = 180
min_thr = 0

sample_time = 2
logging = True
throttle = 5
weight = 100

file_name = "./tests/learning/test_logging"
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

while 1:
    thr = input("Throttle (0, 255): ")
    
    if thr.lower() == "log":
        radius = input("What is the radius of the propeller: ")
        angle = input("What is the blade angle: ")
        trial = input("What is the trial number (1-5): ")
        trial_name = f"{radius}mm_{angle}deg_{trial}"

        print(f"Recording for {sample_time} seconds, on file {file_name}.xlsx, on sheet {trial_name}")

        df = pd.DataFrame({"Time": [], "Weight": [], "Throttle": [], "Average": []}) # Boilerplate for sheet

        index_count = 0
        time_init = time.time()
        logging = True

        while logging:
            time_current = time.time()
            weight += 10

            try:
                index_count += 1
                if index_count == 1:
                    new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": ["=AVERAGE(C$2:C$10000)"]}) # New first row, with average calculation
                
                else:
                    new_row = pd.DataFrame({"Time": [time_current - time_init], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": [""]}) # Gets all the data and formats it into a new data row

                df = pd.concat([df, new_row], ignore_index=True) # Inserts the new row at the end of the main data table

                with pd.ExcelWriter(f"{file_name}.xlsx", mode="a", if_sheet_exists="replace") as writer: # Save the processed data (time, throttle, weight) to excel file and removes the index count
                    df.to_excel(writer, sheet_name=trial_name, index=False)

                print(df)

            except:
                pass # In case of bad formatted data or any error

            if (sample_time - (time_current - time_init)) <= 0: # Stops logging when hits the time limit
                logging = 0
                
    else:
        throttle = thrToThrottle(thr, throttle)
