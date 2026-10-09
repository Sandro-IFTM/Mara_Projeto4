import pandas as pd
import scipy.stats as stats

def executa_tukey_hsd(df_inst, fator):

    """Executa o teste de Tukey HSD e imprime os resultados."""

    grupos_dict = {cat: g['TAXA_MEDIA_IF'].values for cat, g in df_inst.groupby(fator)}
    nomes = list(grupos_dict.keys())
    valores = [grupos_dict[k] for k in nomes]
    res_tukey = stats.tukey_hsd(*valores)
    linhas = []

    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            r1, r2 = nomes[i], nomes[j]
            diff = res_tukey.statistic[i, j]
            pval = res_tukey.pvalue[i, j]
            signif = "Sim (p < 0.05)" if pval < 0.05 else "Não"
            linhas.append({
                'Comparação': f"{r1} vs {r2}",
                'Diferença das Médias (%)': round(diff, 2),
                'p-valor': round(pval, 4),
                'Significante?': signif
            })
            
    df_tukey = pd.DataFrame(linhas)

    return df_tukey
