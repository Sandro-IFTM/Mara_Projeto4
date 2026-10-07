import matplotlib.pyplot as plt
import seaborn as sns

def plota_boxplot_fator(df, df_inst, coluna_fator, titulo_fator, ordem=None):
    """
    Gera um gráfico Boxplot com sobreposição dos pontos dos IFs (stripplot)
    e linha de referência com a Média Geral da Rede Federal.
    """
    # 1. Definir a ordem das categorias no eixo Y
    if ordem is None:
        # Se não informada, ordena de forma decrescente pela média da taxa
        ordem = (
            df_inst.groupby(coluna_fator)['TAXA_CONCLUSAO']
            .mean()
            .sort_values(ascending=False)
            .index.tolist()
        )

    # 2. Calcular a Média Geral Ponderada da Rede Federal (Linha de Referência)
    media_geral_rede = (df['CONCLUINTES'].sum() / df['INGRESSANTES'].sum()) * 100

    # 3. Configurar o tamanho da figura
    plt.figure(figsize=(11, 5.5))
    ax = plt.gca()

    # 4. Desenhar o Boxplot
    sns.boxplot(
        data=df_inst,
        x='TAXA_CONCLUSAO',
        y=coluna_fator,
        order=ordem,
        palette='Blues_r',
        showmeans=True,
        meanprops={
            "marker": "o",
            "markerfacecolor": "red",
            "markeredgecolor": "black",
            "markersize": 7,
            "label": "Média da Classe"
        },
        boxprops=dict(alpha=0.85)
    )

    # 5. Sobrepor a dispersão real de cada IF (Strip Plot)
    sns.stripplot(
        data=df_inst,
        x='TAXA_CONCLUSAO',
        y=coluna_fator,
        order=ordem,
        color='black',
        alpha=0.55,
        jitter=0.2,
        size=5.5
    )

    # 6. Linha vertical de referência (Média Geral da Rede)
    plt.axvline(
        media_geral_rede,
        color='#333333',
        linestyle='--',
        linewidth=1.3,
        label=f'Média Geral da Rede ({media_geral_rede:.1f}%)'
    )

    # 7. Títulos e rótulos
    plt.title(
        f'Distribuição da Taxa de Conclusão por {titulo_fator} nos Institutos Federais',
        fontsize=14,
        weight='bold',
        pad=15
    )
    plt.xlabel('Taxa de Conclusão (%) [Ponto Vermelho = Média | Pontos Pretos = Cada IF]', fontsize=11)
    plt.ylabel('')

    # Grade suave e ajustes visuais
    plt.grid(True, axis='x', linestyle=':', alpha=0.6)
    plt.grid(False, axis='y')
    sns.despine(left=True, bottom=False)

    # Legenda sem duplicidades
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='lower right', frameon=True)

    plt.tight_layout()
    plt.show()
