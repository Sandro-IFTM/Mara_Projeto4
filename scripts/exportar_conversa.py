#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Exportar Histórico de Conversas do Antigravity (Gemini) para Markdown.

Projeto: TCC Mara Oliveira - Projeto 4 (Rede Federal / PNP)
Autor: Equipe de Orientação e Desenvolvimento
Data: Outubro/2026

Uso:
    python scripts/exportar_conversa.py
    python scripts/exportar_conversa.py --output Docs/Conversa_Projeto4.md
    python scripts/exportar_conversa.py --conv-id <ID_DA_CONVERSA>
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

# Diretório padrão onde o Antigravity IDE armazena os logs
DEFAULT_BRAIN_DIR = Path.home() / ".gemini" / "antigravity-ide" / "brain"
DEFAULT_OUTPUT_FILE = Path("Docs") / "Historico_Conversa_Projeto4.md"


def encontrar_conversa_mais_recente(brain_dir: Path) -> Path:
    """Localiza a pasta da conversa mais recentemente atualizada."""
    if not brain_dir.exists():
        raise FileNotFoundError(f"Diretório do Antigravity não encontrado: {brain_dir}")

    candidatos = []
    for d in brain_dir.iterdir():
        if d.is_dir():
            transcript_file = d / ".system_generated" / "logs" / "transcript_full.jsonl"
            if transcript_file.exists():
                candidatos.append((d, transcript_file.stat().st_mtime))

    if not candidatos:
        raise FileNotFoundError("Nenhum arquivo 'transcript_full.jsonl' foi encontrado nas sessões.")

    # Ordena pelo arquivo mais recente
    candidatos.sort(key=lambda x: x[1], reverse=True)
    return candidatos[0][0]


def limpar_texto_usuario(raw_text: str) -> str:
    """Extrai apenas a mensagem real enviada pelo usuário, removendo tags de sistema."""
    if not raw_text:
        return ""

    # Se estiver envolvido pela tag <USER_REQUEST>, extrai o miolo
    match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", raw_text, re.DOTALL)
    if match:
        raw_text = match.group(1)

    # Remove blocos de metadados do sistema (<ADDITIONAL_METADATA>, <USER_SETTINGS_CHANGE>, etc.)
    raw_text = re.sub(r"<[A-Z_]+>.*?</[A-Z_]+>", "", raw_text, flags=re.DOTALL)
    raw_text = re.sub(r"<[A-Z_]+>", "", raw_text)

    # Normaliza quebras de linha no início e fim
    return raw_text.strip()


def extrair_turnos(transcript_path: Path):
    """Lê o transcript_full.jsonl e agrupa as interações em turnos (Usuário -> Assistente)."""
    turnos = []
    current_user_msgs = []
    current_assistant_msgs = []
    turn_timestamp = ""

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            tipo = item.get("type")
            conteudo = (item.get("content") or "").strip()
            created_at = item.get("created_at", "")

            # Mensagem do usuário
            if tipo == "USER_INPUT":
                texto_limpo = limpar_texto_usuario(conteudo)
                if not texto_limpo:
                    continue

                # Se já tínhamos uma resposta do assistente do turno anterior, salva e abre novo turno
                if current_assistant_msgs:
                    turnos.append({
                        "timestamp": turn_timestamp,
                        "user": "\n\n".join(current_user_msgs),
                        "assistant": "\n\n".join(current_assistant_msgs),
                    })
                    current_user_msgs = []
                    current_assistant_msgs = []
                    turn_timestamp = ""

                current_user_msgs.append(texto_limpo)
                if not turn_timestamp:
                    turn_timestamp = created_at

            # Resposta do Assistente
            elif tipo == "PLANNER_RESPONSE" and conteudo:
                # Ignora avisos temporários de execução de ferramentas intermediárias
                if conteudo.startswith("Estou aguardando") or conteudo.startswith("Estou verificando"):
                    continue
                current_assistant_msgs.append(conteudo)

    # Adiciona o último turno em aberto
    if current_user_msgs:
        turnos.append({
            "timestamp": turn_timestamp,
            "user": "\n\n".join(current_user_msgs),
            "assistant": "\n\n".join(current_assistant_msgs) if current_assistant_msgs else "*(Turno em andamento)*",
        })

    return turnos


def formatar_data(iso_str: str) -> str:
    """Formata data ISO para formato legível no Brasil (dd/mm/aaaa hh:mm)."""
    if not iso_str:
        return "N/D"
    try:
        # Tratamento de sufixo Z ou offset
        clean_iso = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        return dt.strftime("%d/%m/%Y às %H:%M:%S")
    except Exception:
        return iso_str


def gerar_markdown(turnos, conv_id: str, titulo: str) -> str:
    """Gera o documento Markdown completo com sumário clicável e corpo formatado."""
    md = []
    data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    # Cabeçalho do documento
    md.append(f"# {titulo}\n")
    md.append("> Documento gerado automaticamente pelo script `exportar_conversa.py`.")
    md.append(f"> \n> **ID da Sessão:** `{conv_id}`  \n> **Data de Exportação:** {data_geracao}  \n> **Total de Interações:** {len(turnos)}\n")
    md.append("---\n")

    # Sumário / Índice
    md.append("## 📑 Sumário das Interações\n")
    for i, t in enumerate(turnos, 1):
        # Cria uma linha de resumo a partir da primeira frase do usuário
        primeira_linha = t["user"].split("\n")[0].strip()
        if len(primeira_linha) > 85:
            primeira_linha = primeira_linha[:82] + "..."
        # Remove caracteres que quebrem markdown link
        primeira_linha_limpa = re.sub(r"[\[\]#*`_]", "", primeira_linha)
        data_formatada = formatar_data(t["timestamp"])
        anchor = f"interacao-{i}"
        md.append(f"{i}. [{primeira_linha_limpa}](#{anchor}) *({data_formatada})*")

    md.append("\n---\n")

    # Corpo com as interações completas
    for i, t in enumerate(turnos, 1):
        data_formatada = formatar_data(t["timestamp"])
        anchor = f"interacao-{i}"

        md.append(f"<a id=\"{anchor}\"></a>")
        md.append(f"## Interação {i:02d} — {data_formatada}\n")

        md.append("### 👤 Usuário:\n")
        md.append(t["user"])
        md.append("\n")

        md.append("### 🤖 Antigravity / Gemini:\n")
        md.append(t["assistant"])
        md.append("\n---\n")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Exporta a transcrição completa de uma sessão do Antigravity/Gemini para Markdown."
    )
    parser.add_argument(
        "--conv-id",
        type=str,
        default=None,
        help="ID específico da conversa. Se omitido, utiliza a sessão mais recente.",
    )
    parser.add_argument(
        "--brain-dir",
        type=Path,
        default=DEFAULT_BRAIN_DIR,
        help="Caminho para o diretório de dados do Antigravity (padrão: ~/.gemini/antigravity-ide/brain).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Arquivo de destino (padrão: {DEFAULT_OUTPUT_FILE}).",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Histórico de Sessão e Orientações — TCC Mara Oliveira (Projeto 4)",
        help="Título principal do documento Markdown.",
    )

    args = parser.parse_args()

    # Configura encoding do console para evitar erro com caracteres em terminais Windows (cp1252)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # 1. Localiza a pasta da conversa
    if args.conv_id:
        conv_dir = args.brain_dir / args.conv_id
        if not conv_dir.exists():
            print(f"[ERRO] Sessao nao encontrada: {conv_dir}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            conv_dir = encontrar_conversa_mais_recente(args.brain_dir)
        except Exception as e:
            print(f"[ERRO] Falha ao localizar sessao recente: {e}", file=sys.stderr)
            sys.exit(1)

    conv_id = conv_dir.name
    transcript_file = conv_dir / ".system_generated" / "logs" / "transcript_full.jsonl"

    if not transcript_file.exists():
        print(f"[ERRO] Arquivo de log nao encontrado: {transcript_file}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Sessao selecionada: {conv_id}")
    print(f"[INFO] Lendo transcricao: {transcript_file}")

    # 2. Extrai os turnos
    turnos = extrair_turnos(transcript_file)
    print(f"[SUCESSO] {len(turnos)} interacoes extraidas e organizadas.")

    # 3. Gera o Markdown formatado
    conteudo_md = gerar_markdown(turnos, conv_id=conv_id, titulo=args.title)

    # 4. Salva no arquivo de saída
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(conteudo_md)

    print(f"[SUCESSO] Conversa exportada com sucesso para:")
    print(f"   -> {args.output.resolve()}")


if __name__ == "__main__":
    main()
