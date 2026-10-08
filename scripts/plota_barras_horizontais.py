# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plota_barras_horizontais(df, tab_fator, fator, titulo_fator, stat='TAXA_MEDIA_GERAL', df_inst=None, paleta_cores=None):
    """
    Gera gráfico de barras horizontais de conclusão (%) por categoria.
    
    Parâmetros:
    -----------
    stat : str ('TAXA_MEDIA_GERAL' ou 'TAXA_MEDIA_IF')
        - 'TAXA_MEDIA_GERAL': Plota a Taxa Ponderada Global (Nível Discente)
        - 'TAXA_MEDIA_IF': Plota a Média Simples Institucional dos IFs (Nível Institucional)
    """
    # 1. Configurar métrica, títulos e linha de referência conforme o tipo
    if stat == 'TAXA_MEDIA_GERAL':
        col_metrica = 'TAXA_MEDIA_GERAL'
        titulo = f'Taxa Ponderada Global de Conclusão por {titulo_fator} (Nível Discente)'
        label_x = 'Taxa Ponderada de Conclusão (%)'
        media_ref = (df['CONCLUINTES'].sum() / df['INGRESSANTES'].sum()) * 100
        rotulo_ref = f'Média Geral da Rede ({media_ref:.1f}%)'
        paleta = paleta_cores if paleta_cores else 'Blues_r'
    else:  # 'TAXA_MEDIA_IF' ou 'TAXA_MEDIA_INST'
        col_metrica = 'TAXA_MEDIA_IF'
        titulo = f'Média Institucional de Conclusão por {titulo_fator} (Nível Institucional)'
        label_x = 'Média Simples das Instituições (%)'
        media_ref = df_inst['TAXA_MEDIA_IF'].mean() if df_inst is not None else tab_fator['TAXA_MEDIA_IF'].mean()
        rotulo_ref = f'Média Institucional dos IFs ({media_ref:.1f}%)'
        paleta = paleta_cores if paleta_cores else 'Blues_r'

    # 2. Ordenar decrescente pela métrica selecionada
    df_plot = tab_fator.sort_values(by=col_metrica, ascending=False).reset_index(drop=True)

    # 3. Altura dinâmica proporcional ao número de categorias
    altura = max(3.0 if fator == 'SEXO' else 4.0, len(df_plot) * 0.65)
    plt.figure(figsize=(10.5, altura))
    ax = plt.gca()

    # 4. Desenhar as barras horizontais
    sns.barplot(
        data=df_plot,
        x=col_metrica,
        y=fator,
        hue=fator,
        order=df_plot[fator],
        palette=paleta,
        legend=False,
        alpha=0.88,
        width=0.80
    )

    # 5. Linha vertical de referência
    plt.axvline(
        media_ref,
        color='#333333',
        linestyle='--',
        linewidth=1.3,
        label=rotulo_ref
    )

    # 6. Rótulos percentuais no interior das barras (SEM letras)
    max_val = df_plot[col_metrica].max()
    for i, row in df_plot.iterrows():
        val = row[col_metrica]
        cor_texto = 'white' if i < (len(df_plot) / 2) else '#1f2d3d'
        ax.text(
            val - 1.0,
            i,
            f'{val:.1f}%',
            va='center',
            ha='right',
            fontsize=10.5,
            fontweight='bold',
            color=cor_texto
        )

    # 7. Formatação visual do gráfico
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    plt.title(titulo, fontsize=13.5, fontweight='bold', loc='left', pad=28)
    plt.xlabel(label_x, fontsize=11, loc='left', labelpad=10)
    plt.ylabel('')
    plt.xlim(0, max_val * 1.05)

    ax.grid(False)
    sns.despine(top=False, bottom=True, left=True, right=True)

    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.08),
        frameon=False,
        fontsize=10.5
    )
    plt.tight_layout()
    plt.show()
