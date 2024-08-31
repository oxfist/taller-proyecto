#!/bin/bash

input_file=$1
output_path=../datasets

echo "Now filtering pagos by partida MINSAL and años 2018-2024..."
awk -F, 'NR == 1 || ($3 ~ "16" && $1 ~ /2018|2019|2020|2021|2022|2023|2024/)' "$input_file" >"$output_path/pagos_salud_2018-2024.csv"
