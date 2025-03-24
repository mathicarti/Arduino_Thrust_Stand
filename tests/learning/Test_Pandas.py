import pandas as pd

df = pd.DataFrame({"Time": [""], "Weight": [""], "Throttle": [""], "Average": ["=AVERAGE(C$3:C$10000)"]})

sample_time = 5
file_name = "./tests/learning/test_logging.xlsx"

radius = input("What is the radius of the propeller: ")
angle = input("What is the blade angle: ")
trial = input("What is the trial number (1-5): ")
trial_name = f"{radius}mm_{angle}deg_{trial}"

print(f"Recording for {sample_time} seconds, on file {file_name}.xlsx, on sheet {trial_name}")

for i in range(10):
    time = 0+i
    weight = 300+i^2
    throttle = 10

    new_row = pd.DataFrame({"Time": [int(time)], "Weight": [int(weight)], "Throttle": [int(throttle)], "Average": [""]})
    df = pd.concat([df, new_row], ignore_index=True)

    with pd.ExcelWriter(file_name, mode='a', if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=trial_name, index=False)

print(df)