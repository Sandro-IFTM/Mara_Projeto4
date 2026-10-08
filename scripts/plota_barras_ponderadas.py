# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns

def plota_barras_ponderadas(df, tab_fator, coluna_fator, titulo_fator):
    """
    Gera um gráfico de barras horizontais com a Taxa Ponderada de Conclusão (%)
    por categoria, ordenado de forma decrescente, com linha de referência da Média da Rede.
    """
    # 1. Média Geral Ponderada da Rede Federal (Linha de Referência)
    media_geral_rede = (df['CONCLUINTES'].sum() / df['INGRESSANTES'].sum()) * 100

    # 2. Ordenar a tabela pela Taxa Ponderada de forma decrescente
    df_plot = tab_fator.sort_values(by='TAXA_PONDERADA', ascending=False).reset_index(drop=True)

    # 3. Configurar a figura com altura dinâmica proporcional ao número de categorias
    altura = max(4.0, len(df_plot) * 0.7)
    plt.figure(figsize=(10.5, altura))
    ax = plt.gca()

    # 4. Desenhar as barras horizontais
    sns.barplot(
        data=df_plot,
        x='TAXA_PONDERADA',
        y=coluna_fator,
        order=df_plot[coluna_fator],
        palette='Blues_r',
        alpha=0.88
    )

    # 5. Linha vertical de referência da Média Geral da Rede
    plt.axvline(
        media_geral_rede,
        color='#333333',
        linestyle='--',
        linewidth=1.3,
        label=f'Média Geral da Rede ({media_geral_rede:.1f}%)'
    )

    # 6. Adicionar rótulos percentuais na ponta das barras
    max_val = df_plot['TAXA_PONDERADA'].max()
    for i, row in df_plot.iterrows():
        val = row['TAXA_PONDERADA']
        ax.text(
            val + 0.8,
            i,
            f'{val:.1f}%',
            va='center',
            ha='left',
            fontsize=10.5,
            fontweight='bold',
            color='#2c3e50'
        )

    # 7. Títulos e formatação visual
    plt.title(
        f'Taxa Ponderada Global de Conclusão por {titulo_fator} (Nível Discente)',
        fontsize=13.5,
        fontweight='bold',
        pad=16,
        loc='left'
    )
    plt.xlabel('Taxa Ponderada de Conclusão (%)', fontsize=11, labelpad=10)
    plt.ylabel('')
    plt.xlim(0, max_val * 1.15)

    plt.grid(True, axis='x', linestyle=':', alpha=0.6)
    plt.grid(False, axis='y')
    sns.despine(top=True, right=True, left=False, bottom=False)

    plt.legend(loc='lower right', frameon=True, fontsize=10.5)
    plt.tight_layout()
    plt.show()
