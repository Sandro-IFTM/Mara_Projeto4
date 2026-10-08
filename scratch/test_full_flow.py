import sys
sys.path.append('d:/MyProjects/IFTM/Orientacao/ECD/2025/Mara_Oliveira/Projeto4/scripts')
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from prepara_dados_fator import prepara_dados_fator
from executa_teste_quiquadrado import executa_teste_quiquadrado
from verifica_pressupostos_anova import verifica_pressupostos_anova
from executa_anova_oneway import executa_anova_oneway
from executa_kruskal_wallis import executa_kruskal_wallis
from executa_tukey_hsd import executa_tukey_hsd
from executa_posthoc_mannwhitney import executa_posthoc_mannwhitney
from plota_boxplot_fator import plota_boxplot_fator
from plota_barras_horizontais import plota_barras_horizontais
from formata_tabela import formata_tabela
from gera_agrup_poshoc import gera_agrup_poshoc

df = pd.read_parquet('d:/MyProjects/IFTM/Orientacao/ECD/2025/Mara_Oliveira/Projeto4/Data/Candidatos_Tratados.parquet')

fatores = ['REGIAO', 'ETNIA', 'FAIXA_ETARIA', 'RENDA', 'SEXO']

for fator in fatores:
    print("=" * 80)
    print(f"ANÁLISE ESTATÍSTICA DESCRITIVA PARA O FATOR: {fator}")
    print("=" * 80)

    # Etapa 01 - Análise Estatística Descritiva
    df_inst, tab_fator = prepara_dados_fator(df, fator)
    formata_tabela(tab_fator, fator)

    # Etapa 02 - Teste Qui-Quadrado e V de Cramér (Nível Discente)
    tab_chi, chi2, p_chi2, v_cramer, intensidade = executa_teste_quiquadrado(df, fator)
    formata_tabela(tab_chi, fator)

    # Etapa 03 - Gráfico de Barras Horizontais das Médias Ponderadas
    plota_barras_horizontais(df, tab_fator, fator, fator, stat='MEDIA_POND')

    # Etapa 04 - Teste de normalidade
    p_shapiro, p_levene = verifica_pressupostos_anova(df_inst, fator)

    # Etapa 05 e 06 - Teste Institucional Global (ANOVA ou Kruskal-Wallis) + Pós-teste
    df_post = None
    if p_shapiro > 0.05 and p_levene > 0.05:
        f_stat, p_global = executa_anova_oneway(df_inst, fator)
        if p_global < 0.05:
            df_post = executa_tukey_hsd(df_inst, fator)
            formata_tabela(df_post, 'Comparação')
    else:
        h_stat, p_global = executa_kruskal_wallis(df_inst, fator)
        if p_global < 0.05:
            if df_inst[fator].nunique() > 2:
                df_post = executa_posthoc_mannwhitney(df_inst, fator)
                formata_tabela(df_post, 'Comparação')

    # Agrupamento Pós-hoc Institucional: Letras CLD e Cores por patamar estatístico
    cld_map, paleta_cores = gera_agrup_poshoc(
        df_inst=df_inst,
        fator=fator,
        df_posthoc=df_post,
        p_global=p_global
    )

    # Tabela com as letras na tabela descritiva
    tab_fator['GRUPO'] = tab_fator[fator].map(cld_map)
    formata_tabela(tab_fator, fator)

    # Etapa 07 - Gráfico de Barras Horizontais das Médias por IF
    plota_barras_horizontais(df, tab_fator, fator, fator, stat='if', df_inst=df_inst, paleta_cores=paleta_cores)

    # Etapa 08 - Gráfico de Boxplot com Strip Plot das Médias por IF
    plota_boxplot_fator(df, df_inst, fator, fator, paleta_cores=paleta_cores)

print("Tudo executado com perfeição!")
