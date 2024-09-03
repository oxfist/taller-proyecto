import os
import pandas as pd

START_YEAR = 2018

file_servicio_mapping = {
    "aconcagua.csv": (27, "SERVICIO DE SALUD ACONCAGUA"),
    "antofagasta.csv": (22, "SERVICIO DE SALUD ANTOFAGASTA"),
    "araucania-norte.csv": (35, "SERVICIO DE SALUD ARAUCANÍA NORTE"),
    "araucania-sur.csv": (36, "SERVICIO DE SALUD ARAUCANÍA SUR"),
    "arauco.csv": (34, "SERVICIO DE SALUD ARAUCO"),
    "arica-parinacota.csv": (20, "SERVICIO DE SALUD ARICA"),
    "atacama.csv": (23, "SERVICIO DE SALUD ATACAMA"),
    "aysen.csv": (40, "SERVICIO DE SALUD AYSÉN"),
    "biobio.csv": (33, "SERVICIO DE SALUD BIO BIO"),
    "chiloe.csv": (53, "SERVICIO DE SALUD CHILOÉ"),
    "concepcion.csv": (31, "SERVICIO DE SALUD CONCEPCIÓN"),
    "coquimbo.csv": (24, "SERVICIO DE SALUD COQUIMBO"),
    "magallanes.csv": (41, "SERVICIO DE SALUD MAGALLANES"),
    "maule.csv": (29, "SERVICIO DE SALUD MAULE"),
    "metropolitano-central.csv": (43, "SERVICIO DE SALUD METROPOLITANO CENTRAL"),
    "metropolitano-norte.csv": (45, "SERVICIO DE SALUD METROPOLITANO NORTE"),
    "metropolitano-occidente.csv": (46, "SERVICIO DE SALUD METROPOLITANO OCCIDENTE"),
    "metropolitano-oriente.csv": (42, "SERVICIO DE SALUD METROPOLITANO ORIENTE"),
    "metropolitano-sur.csv": (44, "SERVICIO DE SALUD METROPOLITANO SUR"),
    "metropolitano-suroriente.csv": (
        47,
        "SERVICIO DE SALUD METROPOLITANO SUR - ORIENTE",
    ),
    "nuble.csv": (30, "SERVICIO DE SALUD ÑUBLE"),
    "ohiggins.csv": (28, "SERVICIO DE SALUD O´HIGGINS"),
    "osorno.csv": (38, "SERVICIO DE SALUD OSORNO"),
    "reloncavi.csv": (39, "SERVICIO DE SALUD DEL RELONCAVI"),
    "talcahuano.csv": (32, "SERVICIO DE SALUD TALCAHUANO"),
    "tarapaca.csv": (21, "SERVICIO DE SALUD TARAPACÁ"),
    "valdivia.csv": (37, "SERVICIO DE SALUD VALDIVIA"),
    "valparaiso-san-antonio.csv": (25, "SERVICIO DE SALUD VAPARAÍSO-SAN ANTONIO"),
    "vina-del-mar-quillota.csv": (26, "SERVICIO DE SALUD VIÑA DEL MAR Y QUILLOTA"),
}


def read_intento_ideacion(path):
    files = [f for f in os.listdir(path)]
    df = pd.DataFrame()
    for f in files:
        new_df = pd.read_csv(f"{path}/{f}", delimiter=",")
        new_df["capitulo"] = file_servicio_mapping[f][0]
        new_df["nombre_capitulo"] = file_servicio_mapping[f][1]
        df = pd.concat([df, new_df])

    df.columns = df.columns.str.lower()
    df = df.pivot_table(
        index=["año", "capitulo", "nombre_capitulo"],
        columns=["glosa"],
        values=["total"],
    ).reset_index()
    df.columns = df.columns.droplevel(1)
    df.columns.values[3] = "suicidio_ideacion"
    df.columns.values[4] = "suicidio_intento"
    return df


def read_urgencia_autolesiones(path):
    files = [f for f in os.listdir(path)]
    df = pd.DataFrame()
    for f in files:
        new_df = pd.read_csv(f"{path}/{f}", delimiter=",")
        new_df["capitulo"] = file_servicio_mapping[f][0]
        new_df["nombre_capitulo"] = file_servicio_mapping[f][1]
        df = pd.concat([df, new_df])

    df.columns = df.columns.str.lower()
    df = df.rename(columns={"total_65_mas": "urgencias_lesiones_autoinflingidas"})
    df = df[
        ["año", "capitulo", "nombre_capitulo", "urgencias_lesiones_autoinflingidas"]
    ]
    df = df.sort_values(by=["año", "capitulo", "nombre_capitulo"])
    return df


def impute_intento_ideacion_with_mean(df):
    missing_year_df = pd.DataFrame(
        {
            "año": [START_YEAR] * len(df["capitulo"].unique()),
            "capitulo": df["capitulo"].unique(),
            "nombre_capitulo": df["nombre_capitulo"].unique(),
            "suicidio_ideacion": [None] * len(df["capitulo"].unique()),
            "suicidio_intento": [None] * len(df["capitulo"].unique()),
        }
    )
    imputed_values = (
        df.groupby("capitulo")[["suicidio_ideacion", "suicidio_intento"]]
        .mean()
        .reset_index()
    )
    print(imputed_values)

    new_df = pd.merge(missing_year_df, imputed_values, on=["capitulo"], how="left")
    new_df["suicidio_ideacion"] = new_df["suicidio_ideacion_x"].fillna(
        new_df["suicidio_ideacion_y"]
    )
    new_df["suicidio_intento"] = new_df["suicidio_intento_x"].fillna(
        new_df["suicidio_intento_y"]
    )
    new_df = new_df[
        ["año", "capitulo", "nombre_capitulo", "suicidio_ideacion", "suicidio_intento"]
    ]
    return pd.concat([new_df, df], ignore_index=True)


def impute_intento_ideacion(df):
    missing_year_df = pd.DataFrame(
        {
            "año": [START_YEAR] * len(df["capitulo"].unique()),
            "capitulo": df["capitulo"].unique(),
            "nombre_capitulo": df["nombre_capitulo"].unique(),
            "suicidio_ideacion": [None] * len(df["capitulo"].unique()),
            "suicidio_intento": [None] * len(df["capitulo"].unique()),
        }
    )
    new_df = pd.concat([missing_year_df, df], ignore_index=True)

    imputed_values = (
        new_df.groupby(["capitulo", "nombre_capitulo"])
        .apply(lambda group: group.interpolate(method="linear", limit_direction="both"))
        .reset_index(drop=True)
        .sort_values(by=["año", "capitulo"])
    )

    return imputed_values


def impute_urgencia_autolesiones(df):
    anio_values = range(START_YEAR, 2024)
    capitulo_values = df[["capitulo", "nombre_capitulo"]].drop_duplicates()

    full_index = pd.MultiIndex.from_product(
        [anio_values, capitulo_values["capitulo"]],
        names=["año", "capitulo"],
    )
    full_df = pd.DataFrame(index=full_index).reset_index()
    full_df = pd.merge(full_df, capitulo_values, on="capitulo", how="left")
    return (
        pd.merge(full_df, df, on=["año", "capitulo", "nombre_capitulo"], how="left")
        .sort_values(by=["año", "capitulo"])
        .fillna(0)
    )


intento_ideacion_df = read_intento_ideacion("../../datasets/ideacion-intento")
intento_ideacion_df = impute_intento_ideacion(intento_ideacion_df)
intento_ideacion_df.to_csv("../../datasets/ideacion_intento.csv", index=False)

urgencia_autolesiones_df = read_urgencia_autolesiones(
    "../../datasets/urgencia-lesiones-autoinflingidas"
)
urgencia_autolesiones_df = impute_urgencia_autolesiones(urgencia_autolesiones_df)
urgencia_autolesiones_df.to_csv(
    "../../datasets/urgencia_lesiones_autoinflingidas.csv", index=False
)
