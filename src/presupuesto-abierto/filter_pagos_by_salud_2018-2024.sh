#!/bin/bash

input_file=$1
output_path=../../datasets
output_file="$output_path/pagos_salud-2018-2024.csv"

if [[ ! -f "$input_file" ]]; then
  echo "ERROR: input file does not exist or is not valid, make sure you include it as an argument."
  exit 1
fi

if [[ ! -s "$input_file" ]]; then
  echo "ERROR: $input_file is empty."
  exit 1
fi

if [[ "${input_file##*.}" != "csv" ]]; then
  echo "ERROR: $input_file is not a CSV file."
  exit 1
fi

echo "INFO: Now filtering pagos by partida MINSAL and años 2018-2024 into path \`$output_file\`..."
awk -F, 'NR == 1 || ($3 ~ "16" && $1 ~ /2018|2019|2020|2021|2022|2023|2024/)' "$input_file" >"$output_file"
