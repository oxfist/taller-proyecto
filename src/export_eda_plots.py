import pandas as pd
import seaborn as sns

YEARS = range(2018, 2024)
EXCLUDED_VARIABLES = [
    # "top_5_dias_hospitalizacion_total_enfermedades_isquémicas_del_corazón",
    # "top_5_dias_hospitalizacion_total_complicaciones_de_la_atención_médica_y_quirúrgica_no_clasificadas_en_otra_parte",
    # "top_5_dias_hospitalizacion_total_asignación_provisoria_de_nuevas_afecciones_de_etiología_incierta",
]


def get_top_k_columns_with_less_zeroes(k, pattern, df):
    promedio_variables = df.filter(like=pattern).columns.to_list()

    zero_counts = df[promedio_variables].apply(lambda col: (col == 0).sum())
    top_k = zero_counts.sort_values(ascending=True).index[:k]
    return top_k.to_list()


def generate_eda_plots(patterns):
    for pattern in patterns:
        top_k_columns_with_less_zeroes = get_top_k_columns_with_less_zeroes(
            10, pattern, joined_df
        )

        analysis_variables = list(
            filter(
                lambda x: x not in EXCLUDED_VARIABLES,
                [
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
                ],
            )
        )

        for year in YEARS:
            plot = sns.pairplot(
                joined_df[joined_df["año"] == year][analysis_variables],
                kind="reg",
                diag_kind="kde",
                plot_kws={"line_kws": {"color": "red"}},
                diag_kws={"color": "red"},
            )

            for ax in plot.axes.flatten():
                ax.set_xlabel(ax.get_xlabel(), rotation=45)
                ax.set_ylabel(ax.get_ylabel(), rotation=45)
                ax.yaxis.get_label().set_horizontalalignment("right")

            plot.figure.suptitle(f"AÑO {year}", y=1.01, fontsize=16)
            plot.savefig(f"../plots/{pattern}/{year}.png", dpi=65)


joined_df = pd.read_csv("../datasets/eda.csv", delimiter=",")
generate_eda_plots(["hospitalizaciones", "hospitalizacion_total", "promedio"])
