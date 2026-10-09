# -*- coding: utf-8 -*-
"""
Script: exportar_saida_analise.py
Objetivo: Extrai os resultados completos (textos, tabelas e gráficos) da última
          execução do notebook analise_descritivas.ipynb e gera um relatório
          consolidado em formato Markdown (Docs/Saida_Analise_Descritiva.md).
"""

import json
import base64
import re
from pathlib import Path


def exportar_saida_analise():
    # 1. Localizar o diretório raiz do projeto
    diretorio_script = Path(__file__).resolve().parent
    raiz_projeto = diretorio_script.parent
    
    caminho_notebook = raiz_projeto / "Notebooks" / "analise_descritivas.ipynb"
    pasta_docs = raiz_projeto / "Docs"
    pasta_figuras = raiz_projeto / "figuras_analise"
    arquivo_saida = pasta_docs / "Saida_Analise_Descritiva.md"
    
    if not caminho_notebook.exists():
        print(f"Erro: Notebook não encontrado em {caminho_notebook}")
        return

    # Garante que as pastas de destino existam
    pasta_figuras.mkdir(parents=True, exist_ok=True)

    # 2. Ler o arquivo do notebook (.ipynb é um JSON)
    with open(caminho_notebook, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # 3. Encontrar a última célula de código que contém saídas
    celula_alvo = None
    for celula in reversed(nb.get("cells", [])):
        if celula.get("cell_type") == "code" and celula.get("outputs"):
            celula_alvo = celula
            break

    if not celula_alvo:
        print("Erro: Nenhuma célula com saídas foi encontrada no notebook.")
        return

    outputs = celula_alvo.get("outputs", [])
    print(f">> Encontrados {len(outputs)} blocos de saída na célula.")

    # 4. Estruturar o documento Markdown
    md_linhas = [
        "# Relatório Consolidado: Análise Estatística Descritiva e Inferencial",
        "",
        "> **Documento gerado automaticamente a partir das saídas do notebook:** `Notebooks/analise_descritivas.ipynb`  ",
        "> **Controle Metodológico:** Nível Discente (Qui-Quadrado / V de Cramér) e Nível Institucional (Gauss-Markov / ANOVA / Kruskal-Wallis)",
        "",
        "---",
        ""
    ]

    fator_atual = "GERAL"
    contador_img = 0

    for out in outputs:
        tipo = out.get("output_type")
        
        # Processa saídas de texto / prints
        if tipo == "stream":
            texto = "".join(out.get("text", []))
            
            # Detecta se iniciou um novo fator
            match_fator = re.search(r"-{10,}\s+([A-Z_]+)\s+-{10,}", texto)
            if match_fator:
                fator_atual = match_fator.group(1)
                md_linhas.append(f"\n## FATOR: {fator_atual}\n")
            
            # Adiciona o texto preservando a formatação das tabelas e números
            texto_limpo = texto.strip()
            if texto_limpo:
                md_linhas.append("```text")
                md_linhas.append(texto_limpo)
                md_linhas.append("```")
                md_linhas.append("")
                
        # Processa saídas de gráficos (PNG codificados em base64)
        elif tipo == "display_data":
            dados = out.get("data", {})
            if "image/png" in dados:
                contador_img += 1
                b64_png = dados["image/png"]
                nome_imagem = f"grafico_{contador_img:02d}_{fator_atual}.png"
                caminho_img = pasta_figuras / nome_imagem
                
                # Salva o arquivo físico PNG
                with open(caminho_img, "wb") as f_img:
                    f_img.write(base64.b64decode(b64_png))
                
                # Adiciona o link da imagem no Markdown
                md_linhas.append(f"![{fator_atual} - Gráfico {contador_img:02d}](../figuras_analise/{nome_imagem})")
                md_linhas.append("")

    # 5. Salvar o arquivo Markdown final
    conteudo_final = "\n".join(md_linhas)
    with open(arquivo_saida, "w", encoding="utf-8") as f_out:
        f_out.write(conteudo_final)

    print("=" * 70)
    print(">> SUCESSO!")
    print(f">> Relatório Markdown salvo em: {arquivo_saida}")
    print(f">> Imagens extraídas e salvas: {contador_img} gráficos em {pasta_figuras}")
    print("=" * 70)


if __name__ == "__main__":
    exportar_saida_analise()
