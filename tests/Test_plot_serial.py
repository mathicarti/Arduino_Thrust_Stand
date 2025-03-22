import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

port = "/dev/cu.usbmodem101"
baud_rate = 9600

# Sets up communication with Arduino
ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(1)

throttle = 0
max_thr = 255
min_thr = 0

time_vals = []
throttle_vals = []
load_vals = []
start_time = time.time()

fig, ax = plt.subplots()
ax.set_ylim(0, 300)  # Set Y-axis range (adjust for expected values)
ax.set_xlim(0, 10)   # Display last 10 seconds of data
throttle_line, = ax.plot([], [], label="Throttle", color="blue")
load_line, = ax.plot([], [], label="Load Cell", color="red")

plt.xlabel("Time (s)")
plt.ylabel("Values")
plt.legend()

def update(frame):
    global start_time

    if ser.in_waiting > 0:  # Check if new data is available
        try:
            data = ser.readline().decode().strip()  # Read and decode serial data
            throttle, load = map(int, data.split(","))  # Expecting "throttle,load"

            current_time = time.time() - start_time  # Calculate elapsed time
            time_vals.append(current_time)
            throttle_vals.append(throttle)
            load_vals.append(load)

            # Keep only the last 10 seconds of data
            if len(time_vals) > 100:
                time_vals.pop(0)
                throttle_vals.pop(0)
                load_vals.pop(0)

            # Update graph data
            throttle_line.set_data(time_vals, throttle_vals)
            load_line.set_data(time_vals, load_vals)
            ax.set_xlim(max(0, current_time - 10), current_time)  # Move x-axis forward

        except ValueError:
            pass  # Ignore any badly formatted data

    return throttle_line, load_line


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
        if thrValue >= 0 and thrValue <= 255:
            futureThr = thrValue
        else:
            futureThr = realThrottle

    elif thrCommand == "TERMINATE":
        futureThr = 0
        print("ESC STOPPED")

    else:
        futureThr = realThrottle
    
    return futureThr

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()

while 1:
    thr = input("Throttle: ")
    throttle = thrToThrottle(thr, throttle)

    ser.write((f"{throttle}T\n").encode()) #Sends to the serial aka Arduino

ser.close()