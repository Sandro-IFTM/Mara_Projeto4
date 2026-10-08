# -*- coding: utf-8 -*-

"""
Este módulo contém a função formata_tabela, que formata a tabela para exibição.
"""

def formata_tabela(tabela, col_texto):
    """
    Formata a tabela para exibição com alinhamento adequado:
    primeira coluna à esquerda e colunas numéricas à direita.
    
    Args:
        tabela (pd.DataFrame): DataFrame com os dados.
        col_texto (str): Nome da coluna de texto.
    """ 
    cols = list(tabela.columns)
    
    # Calcula a largura medindo os valores JÁ FORMATADOS com 2 casas decimais
    w = {}
    for c in cols:
        tam_max_dado = max(
            len(f"{x:.2f}" if isinstance(x, float) else str(x))
            for x in tabela[c]
        )
        w[c] = max(tam_max_dado, len(c)) + 2
    
    # Cabeçalho
    header = f"{cols[0]:<{w[cols[0]]}}" + "".join(f"{c:>{w[c]}}" for c in cols[1:])
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    # Linhas de dados
    for _, r in tabela.iterrows():
        v0 = str(r[cols[0]])
        linha = f"{v0:<{w[cols[0]]}}" + "".join(
            f"{r[c]:>{w[c]}.2f}" if isinstance(r[c], float) else f"{r[c]:>{w[c]}}"
            for c in cols[1:]
        )
        print(linha)
    print("-" * len(header))
