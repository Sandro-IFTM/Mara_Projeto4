def prepara_dados_fator(df, coluna_fator):

    """Agrega a taxa de conclusão por IF e calcula estatísticas descritivas."""

    # Agregação institucional
    df_inst = df.groupby([coluna_fator, 'INST']).agg(
        INGRESSANTES=('INGRESSANTES', 'sum'),
        CONCLUINTES=('CONCLUINTES', 'sum')
    ).reset_index()

    df_inst = df_inst[df_inst['INGRESSANTES'] > 0]
    df_inst['TAXA_CONCLUSAO'] = (df_inst['CONCLUINTES'] / df_inst['INGRESSANTES']) * 100
    
    # Estatística Descritiva entre os IFs
    desc = df_inst.groupby(coluna_fator)['TAXA_CONCLUSAO'].agg(
        N_IFS='count',
        MEDIA='mean',
        DESVIO_PADRAO='std',
        MEDIANA='median',
        MIN='min',
        MAX='max'
    ).reset_index()
    
    # Taxa Ponderada Global da Rede
    tx_global = df.groupby(coluna_fator).agg(
        TOTAL_ING=('INGRESSANTES', 'sum'),
        TOTAL_CONC=('CONCLUINTES', 'sum')
    ).reset_index()

    tx_global['TAXA_PONDERADA'] = (tx_global['TOTAL_CONC'] / tx_global['TOTAL_ING']) * 100

    tabela_desc = desc.merge(tx_global[[coluna_fator, 'TAXA_PONDERADA']], on=coluna_fator)
    tabela_desc = tabela_desc.sort_values(by='MEDIA', ascending=False).reset_index(drop=True)

    return df_inst, tabela_desc