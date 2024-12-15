#!/bin/bash

heuristic_values=("Zero" "Epsilon" "Softmax" "Priority")


exec="./eecbs_MCR"
map_file="random-32-32-20.map"
scen_file="random-32-32-20-random-1.scen"

k_value=50
t_value=60
suboptimality=1.2


for heuristic_value in "${heuristic_values[@]}"; do
    echo "Running with heuristicGuide=$heuristic_value"
    

    output_csv="guide_${heuristic_value}_output.csv"
    output_paths="guide_${heuristic_value}_paths.txt"
    

    for i in {1..100}; do
        echo "Run $i for heuristicGuide=$heuristic_value"
        

        $exec -m $map_file -a $scen_file -o $output_csv --outputPaths=$output_paths -k $k_value -t $t_value --suboptimality=$suboptimality --heuristicGuide=$heuristic_value
    done
done

python3 analyse.py
