# -*- coding: utf-8 -*-
import itertools
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def executa_posthoc_quiquadrado(df, fator):
    """
    Executa comparações múltiplas par a par via Qui-Quadrado 2 x 2 (Nível Discente)
    com correção de Bonferroni e cálculo do V de Cramér para cada par.
    """
    # 1. Totalizar Concluintes e Ingressantes por categoria
    df_chi = df.groupby(fator).agg(
        CONCLUINTES=('CONCLUINTES', 'sum'),
        INGRESSANTES=('INGRESSANTES', 'sum')
    ).reset_index()
    df_chi['RETIDOS'] = df_chi['INGRESSANTES'] - df_chi['CONCLUINTES']
    df_chi['TAXA'] = (df_chi['CONCLUINTES'] / df_chi['INGRESSANTES']) * 100
    df_chi = df_chi.sort_values(by='TAXA', ascending=False).reset_index(drop=True)

    cats = df_chi[fator].tolist()
    if len(cats) <= 2:
        return None

    pares = list(itertools.combinations(cats, 2))
    n_pares = len(pares)

    linhas = []
    for c1, c2 in pares:
        d1 = df_chi[df_chi[fator] == c1].iloc[0]
        d2 = df_chi[df_chi[fator] == c2].iloc[0]

        # Tabela 2 x 2
        tab = [
            [d1['CONCLUINTES'], d1['RETIDOS']],
            [d2['CONCLUINTES'], d2['RETIDOS']]
        ]
        c2_stat, p_val, _, _ = chi2_contingency(tab)

        # Ajuste de Bonferroni
        p_adj = min(1.0, p_val * n_pares)

        # V de Cramér do par
        n_par = d1['INGRESSANTES'] + d2['INGRESSANTES']
        v_par = np.sqrt(c2_stat / n_par) if n_par > 0 else 0.0
        diff = d1['TAXA'] - d2['TAXA']

        # Classificação da intensidade do efeito
        if v_par < 0.10:
            intensidade = "Residual"
        elif v_par < 0.30:
            intensidade = "Moderada"
        else:
            intensidade = "Forte"

        linhas.append({
            'Comparação': f'{c1} vs {c2}',
            'Diferença (%)': diff,
            'p-valor': p_adj,
            'V de Cramér': v_par,
            'Efeito': intensidade,
            'Significante?': 'Sim (p < 0.05)' if p_adj < 0.05 else 'Não'
        })

    return pd.DataFrame(linhas)
