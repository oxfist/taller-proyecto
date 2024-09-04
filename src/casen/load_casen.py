import pandas as pd
from regex import W

YEARS = range(2018, 2024)

normalized_names = {
    "SERVICIO DE SALUD IQUIQUE": "SERVICIO DE SALUD TARAPACÁ",
    "SERVICIO DE SALUD AYSEN DEL GENERAL CARLOS IBAÑEZ": "SERVICIO DE SALUD AYSÉN",
}


def impute_casen(path):
    raw_df = pd.read_csv(
        path,
        converters={
            "nombre_capitulo": lambda value: normalized_names.get(
                value.strip(), value.strip()
            )
        },
    )
    print(raw_df["nombre_capitulo"].unique())

    new_rows = pd.DataFrame(
        [
            (year, capitulo, nombre_capitulo)
            for year in YEARS
            for capitulo, nombre_capitulo in zip(
                raw_df["capitulo"].unique(), raw_df["nombre_capitulo"].unique()
            )
        ],
        columns=["año", "capitulo", "nombre_capitulo"],
    )

    imputed_casen_df = (
        pd.merge(
            raw_df, new_rows, on=["año", "capitulo", "nombre_capitulo"], how="outer"
        )
        .groupby(["capitulo", "nombre_capitulo"])
        .apply(lambda group: group.interpolate(method="linear"))
        .reset_index(drop=True)
    )

    imputed_casen_df = imputed_casen_df.sort_values(
        by=["año", "capitulo"], ascending=True
    ).reset_index(drop=True)

    return imputed_casen_df


casen_df = impute_casen("../../datasets/casen/casen_2017_2022_fonasa.csv")
casen_df.to_csv("../../datasets/casen.csv", index=False)
