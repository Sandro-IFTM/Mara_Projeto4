import sys
sys.path.append('d:/MyProjects/IFTM/Orientacao/ECD/2025/Mara_Oliveira/Projeto4/scripts')
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from prepara_dados_fator import prepara_dados_fator
from executa_anova_oneway import executa_anova_oneway
from executa_tukey_hsd import executa_tukey_hsd
from gera_agrup_poshoc import gera_agrup_poshoc

df = pd.read_parquet('d:/MyProjects/IFTM/Orientacao/ECD/2025/Mara_Oliveira/Projeto4/Data/Candidatos_Tratados.parquet')
df_inst, tab_fator = prepara_dados_fator(df, 'REGIAO')
f_stat, p_glob = executa_anova_oneway(df_inst, 'REGIAO')
df_tukey = executa_tukey_hsd(df_inst, 'REGIAO')
cld_map, paleta_inst = gera_agrup_poshoc(df_inst, 'REGIAO', df_tukey, p_glob)

# 1. Gráfico Ponderado (sem letras no rótulo)
# Paleta do Qui-Quadrado: como p < 0.0001, gradação Blues_r
cores_qui = sns.color_palette('Blues_r', len(tab_fator))
ordem_pond = tab_fator.sort_values(by='TAXA_PONDERADA', ascending=False)['REGIAO'].tolist()
paleta_pond = {cat: cores_qui[i] for i, cat in enumerate(ordem_pond)}

df_pond = tab_fator.sort_values(by='TAXA_PONDERADA', ascending=False).reset_index(drop=True)
media_geral_rede = (df['CONCLUINTES'].sum() / df['INGRESSANTES'].sum()) * 100

plt.figure(figsize=(10.5, 4.0))
ax = plt.gca()
sns.barplot(
    data=df_pond, x='TAXA_PONDERADA', y='REGIAO', hue='REGIAO',
    order=df_pond['REGIAO'], palette=paleta_pond, legend=False, alpha=0.88, width=0.80
)
plt.axvline(media_geral_rede, color='#333333', linestyle='--', linewidth=1.3, label=f'Média Geral da Rede ({media_geral_rede:.1f}%)')
for i, row in df_pond.iterrows():
    val = row['TAXA_PONDERADA']
    cor_txt = 'white' if i < (len(df_pond) / 2) else '#1f2d3d'
    ax.text(val - 1.0, i, f'{val:.1f}%', va='center', ha='right', fontsize=10.5, fontweight='bold', color=cor_txt)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
plt.title('Taxa Ponderada Global de Conclusão por Região (Nível Discente)', fontsize=13.5, fontweight='bold', loc='left', pad=28)
plt.xlabel('Taxa Ponderada de Conclusão (%)', fontsize=11, loc='left', labelpad=10)
plt.ylabel('')
plt.xlim(0, df_pond['TAXA_PONDERADA'].max() * 1.05)
ax.grid(False)
sns.despine(top=False, bottom=True, left=True, right=True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=10.5)
plt.tight_layout()
plt.savefig('scratch/test_barras_ponderada_final.png', dpi=150)
plt.close()

# 2. Institucional (Média por IF)
df_inst_plot = tab_fator.sort_values(by='MEDIA', ascending=False).reset_index(drop=True)
media_inst_rede = df_inst['TAXA_CONCLUSAO'].mean()

plt.figure(figsize=(10.5, 4.0))
ax = plt.gca()
sns.barplot(
    data=df_inst_plot, x='MEDIA', y='REGIAO', hue='REGIAO',
    order=df_inst_plot['REGIAO'], palette=paleta_inst, legend=False, alpha=0.88, width=0.80
)
plt.axvline(media_inst_rede, color='#333333', linestyle='--', linewidth=1.3, label=f'Média Institucional dos IFs ({media_inst_rede:.1f}%)')
for i, row in df_inst_plot.iterrows():
    val = row['MEDIA']
    cor_txt = 'white' if i < (len(df_inst_plot) / 2) else '#1f2d3d'
    ax.text(val - 1.0, i, f'{val:.1f}%', va='center', ha='right', fontsize=10.5, fontweight='bold', color=cor_txt)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
plt.title('Média Institucional de Conclusão por Região (Nível Institucional)', fontsize=13.5, fontweight='bold', loc='left', pad=28)
plt.xlabel('Média Simples das Instituições (%)', fontsize=11, loc='left', labelpad=10)
plt.ylabel('')
plt.xlim(0, df_inst_plot['MEDIA'].max() * 1.05)
ax.grid(False)
sns.despine(top=False, bottom=True, left=True, right=True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=10.5)
plt.tight_layout()
plt.savefig('scratch/test_barras_institucional_final.png', dpi=150)
plt.close()

print('Ambos os graficos gerados com sucesso!')
