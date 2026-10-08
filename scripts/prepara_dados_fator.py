def prepara_dados_fator(df, fator):

    """Agrega a taxa de conclusão por IF e calcula estatísticas descritivas."""

    # Agregação institucional
    df_inst = df.groupby([fator, 'INST']).agg(
        INGRESSANTES=('INGRESSANTES', 'sum'),
        CONCLUINTES=('CONCLUINTES', 'sum')
    ).reset_index()

    df_inst = df_inst[df_inst['INGRESSANTES'] > 0]
    df_inst['TAXA_MEDIA_IF'] = (df_inst['CONCLUINTES'] / df_inst['INGRESSANTES']) * 100
    
    # Estatística Descritiva entre os IFs
    desc = df_inst.groupby(fator)['TAXA_MEDIA_IF'].agg(
        N_IFS='count',
        TAXA_MEDIA_IF='mean',
        DESVIO_PADRAO='std',
        MEDIANA='median',
        MIN='min',
        MAX='max'
    ).reset_index()
    
    # Taxa Média Geral do Fator
    tx_global = df.groupby(fator).agg(
        TOTAL_INGRESSANTES=('INGRESSANTES', 'sum'),
        TOTAL_CONCLUINTES=('CONCLUINTES', 'sum')
    ).reset_index()

    tx_global['TAXA_MEDIA_GERAL'] = (tx_global['TOTAL_CONCLUINTES'] / tx_global['TOTAL_INGRESSANTES']) * 100

    tabela_desc = desc.merge(tx_global[[fator, 'TAXA_MEDIA_GERAL']], on=fator)
    tabela_desc = tabela_desc.sort_values(by='TAXA_MEDIA_IF', ascending=False).reset_index(drop=True)

    return df_inst, tabela_desc