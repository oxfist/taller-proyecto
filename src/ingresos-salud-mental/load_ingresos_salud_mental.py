import os
import pandas as pd

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


def read_urgencias_autolesiones(path):
    files = [f for f in os.listdir(path)]
    df = pd.DataFrame()
    for f in files:
        new_df = pd.read_csv(f"{path}/{f}", delimiter=",")
        new_df["capitulo"] = file_servicio_mapping[f][0]
        new_df["nombre_capitulo"] = file_servicio_mapping[f][1]
        df = pd.concat([df, new_df])

    df.columns = df.columns.str.lower()
    df = df.rename(columns={"total_65_mas": "urgencias_lesiones_autoinflingidas"})
    return df


intento_ideacion_df = read_intento_ideacion("../../datasets/ideacion-intento")
intento_ideacion_df.to_csv("../../datasets/ideacion_intento.csv", index=False)

urgencias_autolesiones_df = read_urgencias_autolesiones(
    "../../datasets/urgencia-lesiones-autoinflingidas"
)
urgencias_autolesiones_df.to_csv(
    "../../datasets/urgencia_lesiones_autoinflingidas.csv", index=False
)
