import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Load comunas-servicios")
parser.add_argument(
    "csv_path", type=str, help="Path to the CSV file containing comunas and servicios"
)

args = parser.parse_args()
comunas_servicios_df = pd.read_csv(args.csv_path, delimiter=";")
