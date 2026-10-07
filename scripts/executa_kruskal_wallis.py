import pandas as pd
import scipy.stats as stats

def executa_kruskal_wallis(df_inst, coluna_fator):

    """Executa o teste de Kruskal-Wallis e imprime os resultados."""

    grupos = [g['TAXA_CONCLUSAO'].values for _, g in df_inst.groupby(coluna_fator)]
    h_stat, p_valor = stats.kruskal(*grupos)

    return h_stat, p_valor