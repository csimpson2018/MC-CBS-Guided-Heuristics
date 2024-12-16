import pandas as pd
import glob
import os
import subprocess
import matplotlib.pyplot as plt


heuristic_values = ["Zero", "Epsilon", "Softmax", "Priority"]
exec_path = "./eecbs_MCR"
map_file = "random-32-32-20.map"
scen_file = "random-32-32-20-random-1.scen"
k_value = 50
t_value = 60
suboptimality = 1.2


results = {heuristic: {} for heuristic in heuristic_values}


def delete_files():
    directory = "."
    csv_files = glob.glob(os.path.join(directory, "guide_*_output.csv"))
    txt_files = glob.glob(os.path.join(directory, "guide_*_paths.txt"))

    files_to_delete = csv_files + txt_files

    for file in files_to_delete:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}. Reason: {e}")

delete_files()

for i in [10,20,30,40,50,60,70,80,90,100]:  # Rollouts
    for heuristic_value in heuristic_values:
        for j in range(i): 
            output_csv = f"guide_{heuristic_value}_output.csv"
            output_paths = f"guide_{heuristic_value}_paths.txt"

            command = [
                exec_path,
                "-m", map_file,
                "-a", scen_file,
                "-o", output_csv,
                "--outputPaths", output_paths,
                "-k", str(k_value),
                "-t", str(t_value),
                "--suboptimality", str(suboptimality),
                "--heuristicGuide", heuristic_value
            ]

            subprocess.run(command)

            df = pd.read_csv(output_csv)

            successful = df[df['solution cost'] != -2]

            # if successful.empty:
            #     print(f"{file}: No successful rows")
            #     continue

            average_runtime = successful['runtime'].mean()
            average_cost_ratio = (successful['solution cost'] / successful['sum of costs']).mean()
            num_successful_rows = successful.shape[0]
            success_rate = num_successful_rows / i


            if i not in results[heuristic_value]:
                results[heuristic_value][i] = {}
            
            results[heuristic_value][i] = {
                "success_rate": success_rate,
                "average_runtime": average_runtime,
                "suboptimality": average_cost_ratio
            }
    
    delete_files()

data = []

for heuristic in heuristic_values:
    for i in results[heuristic]:
        data.append({
            "heuristic": heuristic,
            "rollouts": i,
            "success_rate": results[heuristic][i]["success_rate"],
            "average_runtime": results[heuristic][i]["average_runtime"],
            "suboptimality": results[heuristic][i]["suboptimality"]
        })
print(data)
df_results = pd.DataFrame(data)

plt.figure(figsize=(12, 8))

# Success rate vs number of rollouts
plt.subplot(2, 2, 1)
for heuristic_value in heuristic_values:
    subset = df_results[df_results["heuristic"] == heuristic_value]
    plt.plot(subset["rollouts"], subset["success_rate"], label=heuristic_value, marker='o')
plt.xlabel("Number of Rollouts")
plt.ylabel("Success Rate")
plt.title("Success Rate vs Number of Rollouts")
plt.legend(title="Heuristic Guide")

# Runtime vs number of rollouts
plt.subplot(2, 2, 2)
for heuristic_value in heuristic_values:
    subset = df_results[df_results["heuristic"] == heuristic_value]
    plt.plot(subset["rollouts"], subset["average_runtime"], label=heuristic_value, marker='o')
plt.xlabel("Number of Rollout")
plt.ylabel("Average Runtime (s)")
plt.title("Runtime vs Number of Rollouts")
plt.legend(title="Heuristic Guide")

# Suboptimality vs number of rollouts
plt.subplot(2, 2, 3)
for heuristic_value in heuristic_values:
    subset = df_results[df_results["heuristic"] == heuristic_value]
    plt.plot(subset["rollouts"], subset["suboptimality"], label=heuristic_value, marker='o')
plt.xlabel("Number of Rollouts")
plt.ylabel("Suboptimality")
plt.title("Suboptimality vs Number of Rollouts")
plt.legend(title="Heuristic Guide")


plt.tight_layout()
plt.show()
