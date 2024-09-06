#!/bin/bash

input_path=../../datasets/egresos-hospitalarios
output_path=../../datasets/egresos-hospitalarios
output_file="$output_path/pagos_salud-2017-2024.csv"

if [[ ! -s "$input_path" ]]; then
  echo "ERROR: $input_path is empty."
  exit 1
fi

egresos_csv_files=$(find "$input_path" -type f -name "*.csv" | sort)

if [[ -z "$egresos_csv_files" ]]; then
  echo "ERROR: No CSV files found in $input_path."
  exit 1
fi

for csv_file in $egresos_csv_files; do
  basename=$(basename -- "$csv_file")
  output_file="${output_path}/${basename%.*}_snss_fonasa.csv"
  echo "INFO: Now filtering egresos by establecimiento SNSS and previsión FONASA into path \`$output_file\`..."
  awk -F ';' 'NR == 1 || ($1 !~ /No Pertenecientes/ && $10 == 1)' "$csv_file" >"$output_file"
done
