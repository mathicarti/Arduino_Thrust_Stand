import time
import pandas as pd
from library import thrToThrottle, quick_log, log_data_to_excel, tare

throttle = 0
max_thr = 180
min_thr = 0

sample_time = 5
file_name = ""
file_name = f"{input("What is the file name: ")}.xlsx"

while 1:
    thr = input(f"Throttle ({min_thr}, {max_thr}): ")

    if thr == "quit" or thr == "q":
        throttle = thrToThrottle("0", throttle)
        break

    elif thr == "tare":
        tare()

    elif thr.lower() == "qlog" or thr.lower() == "ql":
        try:
            log_time = input("How long to sample: ")
            quick_log(log_time)
        except:
            quick_log()
    
    elif thr.lower() == "log":
        log_data_to_excel(sample_time, file_name)          

    else:
        thrToThrottle(thr, throttle)