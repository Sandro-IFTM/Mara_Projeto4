import pandas as pd
import scipy.stats as stats

def executa_anova_oneway(df_inst, coluna_fator):
    
    """Executa ANOVA one-way e imprime os resultados."""

    grupos = [g['TAXA_MEDIA_IF'].values for _, g in df_inst.groupby(coluna_fator)]
    f_stat, p_valor = stats.f_oneway(*grupos)

    return f_stat, p_valor