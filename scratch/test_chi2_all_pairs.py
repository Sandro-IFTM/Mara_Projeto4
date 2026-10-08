import itertools
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

df = pd.read_parquet('d:/MyProjects/IFTM/Orientacao/ECD/2025/Mara_Oliveira/Projeto4/Data/Candidatos_Tratados.parquet')

for fator in ['REGIAO', 'ETNIA', 'FAIXA_ETARIA', 'RENDA', 'SEXO']:
    df_chi = df.groupby(fator).agg(
        CONCLUINTES=('CONCLUINTES', 'sum'),
        INGRESSANTES=('INGRESSANTES', 'sum')
    ).reset_index()
    df_chi['RETIDOS'] = df_chi['INGRESSANTES'] - df_chi['CONCLUINTES']
    df_chi['TAXA'] = (df_chi['CONCLUINTES'] / df_chi['INGRESSANTES']) * 100
    df_chi = df_chi.sort_values(by='TAXA', ascending=False).reset_index(drop=True)
    
    cats = df_chi[fator].tolist()
    pares = list(itertools.combinations(cats, 2))
    n_pares = len(pares)
    
    tab_global = df_chi[['CONCLUINTES', 'RETIDOS']].T
    chi2_glob, p_glob, _, _ = chi2_contingency(tab_global)
    
    print(f"=== {fator} (chi2={chi2_glob:.1f}, p={p_glob:.2e}) ===")
    for c1, c2 in pares:
        d1 = df_chi[df_chi[fator] == c1].iloc[0]
        d2 = df_chi[df_chi[fator] == c2].iloc[0]
        tab_2x2 = [[d1['CONCLUINTES'], d1['RETIDOS']], [d2['CONCLUINTES'], d2['RETIDOS']]]
        c2_stat, p_val, _, _ = chi2_contingency(tab_2x2)
        p_adj = min(1.0, p_val * n_pares)
        n_pair = d1['INGRESSANTES'] + d2['INGRESSANTES']
        v_pair = np.sqrt(c2_stat / n_pair)
        diff = d1['TAXA'] - d2['TAXA']
        t1 = d1['TAXA']
        t2 = d2['TAXA']
        print(f"  {c1:15} ({t1:4.1f}%) vs {c2:15} ({t2:4.1f}%): diff={diff:5.1f}% | p_adj={p_adj:.2e} | V={v_pair:.4f}")
