# -*- coding: utf-8 -*-
import string
import itertools
import seaborn as sns


def gera_agrup_poshoc(df_inst=None, fator=None, df_posthoc=None, p_global=1.0, ordem=None, filtrar_residual=False):
    """
    Gera o agrupamento estatístico Compact Letter Display (CLD) e paleta de cores.
    Funciona tanto para ANOVA / Kruskal-Wallis quanto para Qui-Quadrado.
    
    Parâmetros:
    -----------
    ordem : list, opcional
        Lista ordenada decrescente das categorias (se None, calcula via df_inst).
    filtrar_residual : bool, opcional
        Se True, pares com efeito 'Residual' (V < 0.10) compartilham a mesma letra.
    """
    # 1. Definir a ordem das categorias
    if ordem is not None:
        ordem_cat = list(ordem)
    elif df_inst is not None and fator is not None:
        ordem_cat = (
            df_inst.groupby(fator)['TAXA_MEDIA_IF']
            .mean()
            .sort_values(ascending=False)
            .index.tolist()
        )
    else:
        raise ValueError("Informe 'ordem' ou 'df_inst' e 'fator'.")

    k = len(ordem_cat)

    # Caso 1: Teste global NÃO significativo (p >= 0.05)
    if p_global >= 0.05:
        cld_map = {cat: 'a' for cat in ordem_cat}
        paleta_cores = {cat: '#2b5c8f' for cat in ordem_cat}
        return cld_map, paleta_cores

    # Caso 2: Exatamente 2 categorias (ex.: Sexo) com teste global significativo
    if k == 2:
        cld_map = {ordem_cat[0]: 'a', ordem_cat[1]: 'b'}
        cores = sns.color_palette('Blues_r', 2)
        paleta_cores = {ordem_cat[0]: cores[0], ordem_cat[1]: cores[1]}
        return cld_map, paleta_cores

    # Caso 3: Sem pós-teste
    if df_posthoc is None or df_posthoc.empty:
        cld_map = {cat: 'a' for cat in ordem_cat}
        paleta_cores = {cat: '#2b5c8f' for cat in ordem_cat}
        return cld_map, paleta_cores

    # Identificar pares com diferença estatística real
    pares_sig = set()
    for _, row in df_posthoc.iterrows():
        sig = 'Sim' in str(row['Significante?'])
        
        # Se filtrar_residual=True, ignora diferenças com tamanho de efeito Residual
        if filtrar_residual and 'Residual' in str(row.get('Efeito', '')):
            sig = False

        if sig:
            partes = str(row['Comparação']).split(' vs ')
            if len(partes) == 2:
                pares_sig.add(frozenset({partes[0].strip(), partes[1].strip()}))

    # Se nenhum par for significante
    if not pares_sig:
        cld_map = {cat: 'a' for cat in ordem_cat}
        paleta_cores = {cat: '#2b5c8f' for cat in ordem_cat}
        return cld_map, paleta_cores

    # Grafo de NÃO-diferenças
    adj = {c: set([c]) for c in ordem_cat}
    for i in range(k):
        for j in range(i + 1, k):
            c1, c2 = ordem_cat[i], ordem_cat[j]
            if frozenset({c1, c2}) not in pares_sig:
                adj[c1].add(c2)
                adj[c2].add(c1)

    # Cliques maximais (grupos homogêneos)
    cliques = []
    for r in range(k, 0, -1):
        for comb in itertools.combinations(ordem_cat, r):
            s = set(comb)
            if all(c2 in adj[c1] for c1, c2 in itertools.combinations(comb, 2)):
                if not any(s.issubset(existing) for existing in cliques):
                    cliques.append(s)

    cliques.sort(key=lambda cl: min(ordem_cat.index(c) for c in cl))

    # Atribuição de letras (a, b, c, ...)
    letras = list(string.ascii_lowercase)
    letras_cat = {c: [] for c in ordem_cat}
    for idx, cl in enumerate(cliques):
        letra = letras[idx % len(letras)]
        for c in cl:
            letras_cat[c].append(letra)

    cld_map = {c: ''.join(sorted(letras_cat[c])) for c in ordem_cat}

    # Atribuição de cores
    grupos_unicos = list(dict.fromkeys(cld_map.values()))
    if len(grupos_unicos) == 1:
        paleta_grupos = {grupos_unicos[0]: '#2b5c8f'}
    else:
        cores = sns.color_palette('Blues_r', len(grupos_unicos))
        paleta_grupos = {grp: cores[i] for i, grp in enumerate(grupos_unicos)}

    paleta_cores = {cat: paleta_grupos[cld_map[cat]] for cat in cld_map}

    return cld_map, paleta_cores
