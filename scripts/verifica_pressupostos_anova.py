import scipy.stats as stats
import pandas as pd

def verifica_pressupostos_anova(df_inst, coluna_fator):

    """Verifica os pressupostos de normalidade e homocedasticidade para ANOVA."""

    grupos_dict = {cat: g['TAXA_CONCLUSAO'].values for cat, g in df_inst.groupby(coluna_fator)}
    valores = list(grupos_dict.values())

    # Normalidade dos resíduos do modelo
    medias = df_inst.groupby(coluna_fator)['TAXA_CONCLUSAO'].transform('mean')
    residuos = df_inst['TAXA_CONCLUSAO'] - medias
    w_shapiro, p_shapiro = stats.shapiro(residuos)

    # Homocedasticidade (Teste de Levene)
    w_levene, p_levene = stats.levene(*valores)
  
    return [p_shapiro, p_levene]