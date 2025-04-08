import pandas as pd

def analyze_excel_blocks_to_excel_aligned(input_file_path, sheet_name, output_file_path):
    try:
        df = pd.read_excel(input_file_path, sheet_name=sheet_name, header=None)
    except FileNotFoundError:
        return "Error: Input file not found."

    throttle_values = []
    mean_weights = []
    start_of_block = 0
    total_columns = df.shape[1]

    while start_of_block < total_columns:
        end_of_block = start_of_block
        while end_of_block < total_columns and not df.iloc[:, end_of_block].isnull().all():
            end_of_block += 1

        current_block = df.iloc[:, start_of_block:end_of_block].dropna(axis=0, how='all')

        if not current_block.empty:
            try:
                current_block.columns = ['time', 'weight', 'throttle', 'thrust']
                current_block['weight_numeric'] = pd.to_numeric(current_block['weight'], errors='coerce')
                valid_weight_data = current_block.dropna(subset=['weight_numeric'])

                if not valid_weight_data.empty:
                    avg_weight = valid_weight_data['weight_numeric'].mean()
                    unique_throttles = current_block['throttle'].unique().tolist()

                    throttle_value = None
                    for throttle in unique_throttles:
                        try:
                            throttle_value = int(float(throttle))
                            break
                        except (ValueError, TypeError):
                            continue

                    if throttle_value is not None:
                        throttle_values.append(throttle_value)
                        mean_weights.append(float(f"{avg_weight:.3f}"))
                    else:
                        print(f"Warning: No valid integer throttle found in block starting at column {start_of_block}.")
                else:
                    print(f"Warning: No valid weight data in block starting at column {start_of_block}.")

            except ValueError:
                print(f"Warning: Problem naming columns in block starting at column {start_of_block}.")

        start_of_block = end_of_block + 1

    # Create a Pandas DataFrame with aligned columns
    output_df = pd.DataFrame({'Throttle': throttle_values, 'Mean Weight': mean_weights})

    # Write the DataFrame to a new Excel file
    try:
        output_df.to_excel(output_file_path, index=False)
        print(f"\nAnalysis results written to: {output_file_path}")
    except Exception as e:
        print(f"Error writing to Excel file: {e}")

# Example usage:

input_excel_file = 'test.xlsx'
radius = input("What was the radius of the prop: ")
angle = input("What was the blade angle: ")
trial = input("What was the trial number (1-5): ")
input_sheet = f"{radius}mm_{angle}deg_trial{trial}"
output_excel_file = 'sum.xlsx'

analyze_excel_blocks_to_excel_aligned(input_excel_file, input_sheet, output_excel_file)
