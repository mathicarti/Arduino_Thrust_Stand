import pandas as pd

data = {
    "Time": [1, 2, 3, 4],
    "Thrust": [10, 11, 13, 10],
    "Throttle": [25, 25, 25, 25],
    "Average": ["=AVERAGE(C$2:C$10000)", 0, 0, 0]
}

df = pd.DataFrame(data)

# new_row = pd.DataFrame({"Time": [5], "Thrust": [12], "Throttle": [25]})

# df = pd.concat([df, new_row], ignore_index=True)

# df.to_csv('test_data.csv', index=False)

# df_read = pd.read_csv('test_data.csv')

# print(df_read)

sample_time = 30
file_name = "test_data"

radius = input("What is the radius of the propeller: ")
angle = input("What is the blade angle: ")
trial = input("What is the trial number (1-5): ")
trial_name = f"{radius}mm_{angle}deg_{trial}"

print(f"Recording for {sample_time} seconds, on file {file_name}.xlsx, on sheet {trial_name}")

with pd.ExcelWriter(f"{file_name}.xlsx", mode='a', if_sheet_exists="new") as writer:
    df.to_excel(writer, sheet_name=trial_name, index=False)

print(df)