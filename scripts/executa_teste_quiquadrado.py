# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def executa_teste_quiquadrado(df, fator):
    """
    Executa o teste Qui-quadrado de Independência (Nível Discente),
    calcula o Tamanho do Efeito (V de Cramér) com classificação de intensidade
    e gera a Tabela de Contingência Discente (Concluintes x Ingressantes).
    """
    # 1. Totalizar Concluintes e Ingressantes por categoria
    df_chi = df.groupby(fator).agg(
        CONCLUINTES=('CONCLUINTES', 'sum'),
        INGRESSANTES=('INGRESSANTES', 'sum')
    ).reset_index()

    # 2. Calcular Retidos / Evadidos e a Taxa Ponderada Real
    df_chi['RETIDOS'] = df_chi['INGRESSANTES'] - df_chi['CONCLUINTES']
    df_chi['TAXA_MEDIA_GERAL'] = (df_chi['CONCLUINTES'] / df_chi['INGRESSANTES']) * 100

    # Ordenar pela Taxa Ponderada de forma decrescente
    df_chi = df_chi.sort_values(by='TAXA_MEDIA_GERAL', ascending=False).reset_index(drop=True)

    # 3. Tabela de Contingência 2 x K para o teste
    tabela_contingencia = df_chi[['CONCLUINTES', 'RETIDOS']].T
    tabela_contingencia.columns = df_chi[fator]

    chi2, p_valor, gl, _ = chi2_contingency(tabela_contingencia)

    # 4. Cálculo do Tamanho do Efeito (V de Cramér)
    n_total = df_chi['INGRESSANTES'].sum()
    v_cramer = np.sqrt(chi2 / n_total) if n_total > 0 else 0.0

    # 5. Classificação da intensidade do efeito
    if v_cramer < 0.10:
        intensidade = "Residual"
    elif v_cramer < 0.30:
        intensidade = "Moderada"
    else:
        intensidade = "Forte"

    # 6. Tabela formatada para exibição (1º item do retorno)
    tab_chi = df_chi[[fator, 'CONCLUINTES', 'RETIDOS', 'INGRESSANTES', 'TAXA_MEDIA_GERAL']]

    return tab_chi, chi2, p_valor, v_cramer, intensidade
