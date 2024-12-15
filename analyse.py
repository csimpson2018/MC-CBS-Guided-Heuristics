import pandas as pd
import glob


csv_files = glob.glob('*.csv')


for file in csv_files:
 
    df = pd.read_csv(file)

    successful = df[df['solution cost'] != -2]
    
    if successful.empty:
        print(f"{file}: No successful rows")
        continue
    
    average_runtime = successful['runtime'].mean()

    average_cost_ratio = (successful['solution cost'] / successful['sum of costs']).mean()

    num_successful_rows = successful.shape[0]

    print(f"Results for {file}:")
    print(f"  Success Rate: {num_successful_rows} out of 100")
    print(f"  Average runtime of successful attempts: {average_runtime}")
    print(f"  Average of (solution cost / sum of costs) for successful attempts - Suboptimality: {average_cost_ratio}\n")
