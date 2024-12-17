import pandas as pd
import glob
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np


heuristic_values = ["Zero", "Epsilon", "Softmax", "Priority"]
exec_path = "./eecbs_MCR"
map_file = "./compare_folder/room-32-32-4.map-scen-random/room-32-32-4.map"
#scen_file = "random-32-32-20-random-1.scen"
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
map_folder="./compare_folder/room-32-32-4.map-scen-random/scen-random"
scenarios = glob.glob(os.path.join(map_folder, "*.scen")) 

#calculate the success rate for all the scenarros for that rollout
     #1/25 success rate..min run time & suboptimality for that scenario in any rollout. #if not successful maximum runtime , cant assign the suboptimality. 
     #check only common scenarios for each solver & then compare
     #ignore that scenarios if solvers havent solved anything common

            #how to calculate the success rate
            #runtime & suboptimality only for succesful ones or everything

for heuristic_value in heuristic_values:
    for num_rollouts in [1,2, 4, 8, 16, 32, 96]:  # Rollouts
        scenario_success = 0  # Count of successful scenarios
        total_scenarios = len(scenarios)

        best_runtime_overall = float("inf")
        best_suboptimality_overall = float("inf")
        
        for scen_file in scenarios:
            print(scen_file)
            scenario_success_flag = False  # Track if this scenario is solved
            
            for rollout in range(num_rollouts):
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

                successful = df[(df['solution cost'] > 0)]
                
                if not successful.empty:
                    scenario_success_flag = True  # Mark this scenario as solved
                    best_runtime_overall = min(best_runtime_overall, successful['runtime'].min())
                    best_suboptimality_overall = min(
                        best_suboptimality_overall,
                        (successful['solution cost'] / successful['sum of costs']).min()
                    )
            print("Completed")

            if scenario_success_flag:
                scenario_success += 1

        if num_rollouts not in results[heuristic_value]:
            results[heuristic_value][num_rollouts] = {}

        results[heuristic_value][num_rollouts] = {
            "success_rate": scenario_success / total_scenarios,
            "runtime": best_runtime_overall if best_runtime_overall != float("inf") else None,
            "suboptimality": best_suboptimality_overall if best_suboptimality_overall != float("inf") else None
        }

    delete_files()

data = []

for heuristic in heuristic_values:
    for i in results[heuristic]:
        data.append({
            "heuristic": heuristic,
            "rollouts": i,
            "success_rate": results[heuristic][i]["success_rate"],
            "runtime": results[heuristic][i]["runtime"],
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
    plt.plot(subset["rollouts"], subset["runtime"], label=heuristic_value, marker='o')
plt.xlabel("Number of Rollout")
plt.ylabel("Runtime (s)")
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
