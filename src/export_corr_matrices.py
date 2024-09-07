import pandas as pd
import plotly.express as px

YEARS = range(2018, 2024)


def get_top_k_columns_with_less_zeroes(k, pattern, df):
    promedio_variables = df.filter(like=pattern).columns.to_list()

    zero_counts = df[promedio_variables].apply(lambda col: (col == 0).sum())
    top_k = zero_counts.sort_values(ascending=True).index[:k]
    return top_k.to_list()


def generate_corr_matrices(patterns):
    for pattern in patterns:
        top_k_columns_with_less_zeroes = get_top_k_columns_with_less_zeroes(
            10, pattern, joined_df
        )

        ANALYSIS_VARIABLES = [
            "gastos_en_personal",
            "bienes_y_servicios_de_consumo",
            "prestaciones_de_seguridad_social",
            "transferencias_corrientes",
            "otros_gastos_corrientes",
            "adquisicion_de_activos_no_financieros",
            "iniciativas_de_inversion",
            "total_gasto",
            "suicidio_ideacion",
            "suicidio_intento",
            "urgencias_lesiones_autoinflingidas",
            "total_fonasa",
            "problemas_llegar_consulta_si",
            "problemas_conseguir_cita_si",
            "problemas_ser_atendido_si",
            "problemas_pagar_por_costo_si",
            *top_k_columns_with_less_zeroes,
        ]

        for year in YEARS:
            corr_matrix = joined_df[joined_df["año"] == year][ANALYSIS_VARIABLES].corr()

            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale="Plasma_r",
                aspect="auto",
                labels=dict(color="Correlación"),
                title=year,
            )
            fig.update_layout(height=1500, width=2500)
            fig.update_xaxes(tickangle=-45)
            fig.update_yaxes(tickangle=-45)

            fig.write_image(f"../plots/corr_matrices/{pattern}/{year}.png", scale=3)


joined_df = pd.read_csv("../datasets/eda.csv", delimiter=",")

generate_corr_matrices(["hospitalizaciones", "hospitalizacion_total", "promedio"])
