import matplotlib.pyplot as plt
import seaborn as sns

def plota_boxplot_fator(df, df_inst, fator, titulo_fator, ordem=None, paleta_cores=None):
    """
    Gera um gráfico Boxplot com sobreposição dos pontos dos IFs (stripplot)
    e linha de referência com a Média Geral da Rede Federal.
    """
    # 1. Definir a ordem das categorias no eixo Y
    if ordem is None:
        # Se não informada, ordena de forma decrescente pela média da taxa
        ordem = (
            df_inst.groupby(fator)['TAXA_MEDIA_IF']
            .mean()
            .sort_values(ascending=False)
            .index.tolist()
        )

    # 2. Média Simples Institucional de todos os IFs da Rede Federal
    media_inst = df_inst['TAXA_MEDIA_IF'].mean()

    # 3. Configurar o tamanho da figura com altura dinâmica proporcional ao número de categorias
    if fator == 'SEXO':
        altura = max(3.0, len(ordem) * 0.75)
    else:
        altura = max(4.0, len(ordem) * 0.75)
    
    plt.figure(figsize=(11, altura))
    ax = plt.gca()

    # 4. Desenhar o Boxplot
    sns.boxplot(
        data=df_inst,
        x='TAXA_MEDIA_IF',
        y=fator,
        order=ordem,
        palette=paleta_cores if paleta_cores else 'Blues_r',
        width=0.80,
        showmeans=True,
        showfliers=False,
        meanprops={
            "marker": "o",
            "markerfacecolor": "red",
            "markeredgecolor": "black",
            "markersize": 7,
            "label": f"Taxa média de conclusão dos IFs por {fator}"
        },
        boxprops=dict(alpha=0.85)
    )

    # 5. Sobrepor a dispersão real de cada IF (Strip Plot)
    sns.stripplot(
        data=df_inst,
        x='TAXA_MEDIA_IF',
        y=fator,
        order=ordem,
        color='black',
        alpha=0.55,
        jitter=0.2,
        size=5.5
    )

    # 6. Linha vertical de referência (Média Geral da Rede)
    plt.axvline(
        media_inst,
        color='#333333',
        linestyle='--',
        linewidth=1.3,
        label=f'Taxa média de conclusão dos IFs ({media_inst:.1f}%)'
    )

    # 7. Títulos e rótulos
    # Move o eixo X para a parte superior
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    plt.title(
        f'Distribuição das taxas médias de conclusão dos IFs por {titulo_fator}',
        fontsize=14,
        weight='bold',
        loc='left',
        pad=28
    )
    plt.xlabel(
        'Taxa média de conclusão dos IFs (%) [Ponto Vermelho] | Taxa de conclusão de cada IF [Pontos Pretos]',
        fontsize=11,
        loc='left',
        labelpad=10
    )
    plt.ylabel('')

    # Grade suave e ajustes visuais
    plt.grid(True, axis='x', linestyle=':', alpha=0.6)
    plt.grid(False, axis='y')
    sns.despine(top=False, bottom=True, left=True, right=True)

    # Legenda sem duplicidades na parte inferior fora do gráfico
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))

    plt.legend(
        by_label.values(),
        by_label.keys(),
        bbox_to_anchor=(1, -0.08),  # 0.5 = centro horizontal; -0.08 = logo abaixo do gráfico
        ncol=2,                       # Posiciona os dois itens lado a lado na horizontal
        frameon=False,                # Sem borda para um visual mais leve e limpo
        fontsize=10.5
    )

    plt.tight_layout()
    plt.show()

