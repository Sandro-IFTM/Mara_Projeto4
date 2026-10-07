import pandas as pd
from scipy.stats import chi2_contingency

def executa_teste_quiquadrado(df, coluna_fator):

    """Executa o teste Qui-quadrado e imprime os resultados."""

    # 1. Totalizar Concluintes e Ingressantes da classe
    df_chi = df.groupby(coluna_fator).agg(
        CONCLUINTES=('CONCLUINTES', 'sum'),
        INGRESSANTES=('INGRESSANTES', 'sum')
    ).reset_index()
    
    # 2. Calcular Não Concluintes (Retenção/Evasão)
    df_chi['NAO_CONCLUINTES'] = df_chi['INGRESSANTES'] - df_chi['CONCLUINTES']
    
    # 3. Tabela de Contingência 2 x K
    tabela_contingencia = df_chi[['CONCLUINTES', 'NAO_CONCLUINTES']].T
    tabela_contingencia.columns = df_chi[coluna_fator]
    
    chi2, p_valor, gl, _ = chi2_contingency(tabela_contingencia)
    
    return chi2, p_valor
