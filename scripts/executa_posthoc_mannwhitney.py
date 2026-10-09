import itertools
import numpy as np
import pandas as pd
import scipy.stats as stats


def executa_posthoc_mannwhitney(df_inst, fator):
    """
    Executa comparações múltiplas par a par não-paramétricas utilizando o teste
    U de Mann-Whitney com correção de Bonferroni para controle de erro Tipo I (FWER).
    
    Parâmetros:
    -----------
    df_inst : pd.DataFrame
        DataFrame agregado por instituição contendo a coluna 'TAXA_MEDIA_IF' e o fator.
    fator : str
        Nome da coluna categórica (ex.: 'RACA', 'FAIXA_ETARIA', 'RENDA', 'SEXO').
        
    Retorno:
    --------
    pd.DataFrame
        Tabela com pares comparados, diferença de medianas, estatística U, p-valores e significância.
    """
    # 1. Separação dos valores por grupo
    grupos_dict = {cat: g['TAXA_MEDIA_IF'].values for cat, g in df_inst.groupby(fator)}
    nomes = list(grupos_dict.keys())
    
    # 2. Gera todos os pares únicos
    pares = list(itertools.combinations(nomes, 2))
    num_comparacoes = len(pares)
    
    if num_comparacoes == 0:
        print("Aviso: Número insuficiente de grupos para comparação par a par.")
        return pd.DataFrame()
    
    linhas = []
    
    for g1, g2 in pares:
        v1 = grupos_dict[g1]
        v2 = grupos_dict[g2]
        
        # Estatística de Mann-Whitney bicaudal
        stat_u, p_bruto = stats.mannwhitneyu(v1, v2, alternative='two-sided')
        
        # Correção de Bonferroni: p_adj = min(1.0, p_bruto * num_comparacoes)
        p_ajustado = min(1.0, p_bruto * num_comparacoes)
        
        # Diferença entre as medianas (%)
        med1 = np.median(v1)
        med2 = np.median(v2)
        dif_medianas = med1 - med2
        
        significante = "Sim (p < 0.05)" if p_ajustado < 0.05 else "Não"
        
        linhas.append({
            'Comparação': f"{g1} vs {g2}",
            'Dif. Medianas (%)': round(dif_medianas, 2),
            'Estatística U': round(stat_u, 1),
            'p-valor Bruto': round(p_bruto, 4),
            'p-valor Ajustado': round(p_ajustado, 4),
            'Significante?': significante
        })
        
    df_posthoc = pd.DataFrame(linhas)
    
    return df_posthoc
