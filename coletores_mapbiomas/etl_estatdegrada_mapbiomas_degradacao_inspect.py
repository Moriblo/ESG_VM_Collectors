# ------------------------------------------------------------
# 📦 ETL MapBiomas — Inspeção de planilha e atualização semântica
# ------------------------------------------------------------

import os
import requests
import zipfile
import io
import json
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

from semantica_mapbiomas import (
    carregar_cache_local,
    atualizar_cache_com_legenda,
    buscar_definicao
)

# ------------------------------------------------------------
# 🔧 Carregar configurações globais
# ------------------------------------------------------------

def carregar_config_global(caminho="setup.json"):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

cfg = carregar_config_global()

ARQUIVO_PERFIS = cfg.get("arquivo_perfis", "perfis_xlsx.json")
atualizar_json = cfg.get("atualizar_json", True)
FORMATO_TIMESTAMP = cfg.get("backup_timestamp_format", "%y%m%d%H%M%S")
PREFIXO_BACKUP = cfg.get("backup_prefix", "perfis_xlsx_bkp")

# ------------------------------------------------------------
# 🧠 Carregar perfil ativo e estrutura do JSON
# ------------------------------------------------------------

def carregar_perfil(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            perfis = json.load(f)
        perfil_ativo = perfis.get("PERFIL_ATIVO")
        dados_perfil = perfis.get(perfil_ativo, {})
        config = dados_perfil.get("config", {})
        dicionario = dados_perfil.get("dicionario", {})
        interpreta_ano = dados_perfil.get("interpreta_ano", "Ano {ano} (sem descrição definida)")
        return perfil_ativo, perfis, config, dicionario, interpreta_ano
    except Exception as e:
        print(f"⚠️ Erro ao carregar JSON de perfis: {e}")
        return None, {}, {}, {}, "Ano {ano} (sem descrição definida)"

PERFIL_ATIVO, TODOS_PERFIS, CONFIG, MAPEAMENTO_CAMPOS, INTERPRETA_ANO = carregar_perfil(ARQUIVO_PERFIS)
URL_ZIP = CONFIG.get("url_zip")
PASTA_DADOS = CONFIG.get("pasta_dados")
ARQUIVO_ALVO = CONFIG.get("arquivo_alvo")

# ------------------------------------------------------------
# 🧼 Limpar pasta de extração antes da execução
# ------------------------------------------------------------

def limpar_pasta_inicio(pasta):
    print("\n🧼 Verificando pasta de dados...")
    os.makedirs(pasta, exist_ok=True)
    arquivos = os.listdir(pasta)
    if not arquivos:
        print("✅ Pasta já está limpa.")
        return
    print(f"⚠️ Removendo {len(arquivos)} arquivos existentes...")
    for arquivo in tqdm(arquivos, desc="🧹 Limpando pasta", ncols=80):
        try:
            os.remove(os.path.join(pasta, arquivo))
        except Exception as e:
            print(f"⚠️ Erro ao remover {arquivo}: {e}")
    print("✅ Pasta limpa com sucesso.")

# ------------------------------------------------------------
# 📥 Download e extração do ZIP com barra de progresso
# ------------------------------------------------------------

def baixar_e_extrair_zip(url, destino):
    print("\n📥 Baixando ZIP...")
    res = requests.get(url, stream=True)
    total = int(res.headers.get('content-length', 0))
    buffer = io.BytesIO()
    progresso = tqdm(total=total, unit='B', unit_scale=True, desc='📦 Download', ncols=80)
    for chunk in res.iter_content(1024 * 64):
        buffer.write(chunk)
        progresso.update(len(chunk))
    progresso.close()
    print("🧩 Extraindo conteúdo do ZIP...")
    with zipfile.ZipFile(buffer) as z:
        z.extractall(destino)
    print("✅ Arquivos extraídos.")

# ------------------------------------------------------------
# 📘 Inspecionar planilha e listar campos detectados
# ------------------------------------------------------------

def inspecionar_planilha(caminho_arquivo):
    print(f"\n📄 Inspecionando planilha vinculada ao perfil: `{PERFIL_ATIVO}`")
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"❌ Planilha não encontrada: {caminho_arquivo}")
    xls = pd.ExcelFile(caminho_arquivo, engine="openpyxl")
    aba = xls.sheet_names[0]
    df = pd.read_excel(xls, sheet_name=aba, nrows=5, engine="openpyxl")
    xls.close()
    colunas = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    print(f"🧾 Planilha: {os.path.basename(caminho_arquivo)} | Aba: {aba}")
    print("📑 Campos detectados:\n")
    for col in colunas:
        if col.isdigit() and 1980 <= int(col) <= 2100:
            print(f"🔹 {col}: {INTERPRETA_ANO.replace('{ano}', col)}")
        elif col in MAPEAMENTO_CAMPOS:
            print(f"🔹 {col}: {MAPEAMENTO_CAMPOS[col]}")
        else:
            print(f"🔹 {col}: ❓ Definir significado")
    return colunas

# ------------------------------------------------------------
# 🔄 Atualizar dicionário com os campos reais + definições semânticas
# ------------------------------------------------------------

def atualizar_dicionario_json(colunas):
    print("\n📁 Atualizando dicionário do perfil ativo...")
    if cfg.get("usar_legenda_csv", True):
        print("📥 Atualizando cache com legenda oficial...")
        atualizar_cache_com_legenda()

    referencias = carregar_cache_local(cfg.get("cache_referencias_path"))
    try:
        with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as f:
            original = json.load(f)
        timestamp = datetime.now().strftime(FORMATO_TIMESTAMP)
        pa_id = original.get(PERFIL_ATIVO, {}).get("PA_ID", "000")
        nome_backup = f"{PREFIXO_BACKUP}_{timestamp}_{pa_id}.json"
        with open(nome_backup, "w", encoding="utf-8") as bkp:
            json.dump(original, bkp, indent=2, ensure_ascii=False)
        print(f"🧷 Backup salvo como: {nome_backup}")
        novo_dicionario = {}
        for col in colunas:
            if col.isdigit() and 1980 <= int(col) <= 2100:
                continue
            desc = MAPEAMENTO_CAMPOS.get(col) or buscar_definicao(col, referencias)
            novo_dicionario[col] = desc
        original[PERFIL_ATIVO]["dicionario"] = novo_dicionario
        with open(ARQUIVO_PERFIS, "w", encoding="utf-8") as f_final:
            json.dump(original, f_final, indent=2, ensure_ascii=False)
        print("✅ JSON atualizado com os campos reais e definições.")
    except Exception as e:
        print(f"⚠️ Erro ao atualizar JSON: {e}")

# ------------------------------------------------------------
# 👁️ Comparar estrutura JSON vs campos reais da planilha
# ------------------------------------------------------------

def comparar_dicionario(colunas):
    json_campos = set(MAPEAMENTO_CAMPOS.keys())
    campos_planilha = set(c for c in colunas if not (c.isdigit() and 1980 <= int(c) <= 2100))
    extras_json = sorted(json_campos - campos_planilha)
    extras_planilha = sorted(campos_planilha - json_campos)
    print("\n📊 Comparativo entre JSON e planilha:")
    if extras_json:
        print("\n🔺 Presentes no JSON, mas ausentes na planilha:")
        for c in extras_json:
            print(f"   ⚠️ {c}")
    if extras_planilha:
        print("\n🔹 Presentes na planilha, mas ausentes no JSON:")
        for c in extras_planilha:
            print(f"   ❓ {c}")
    if not extras_json and not extras_planilha:
        print("✅ JSON está sincronizado com a planilha.")

# ------------------------------------------------------------
# 🧹 Remover arquivos extraídos após o uso
# ------------------------------------------------------------

def limpar_arquivos_finais(pasta):
    arquivos = os.listdir(pasta)
    for arquivo in tqdm(arquivos, desc="🧼 Limpando arquivos finais", ncols=80):
        try:
            os.remove(os.path.join(pasta, arquivo))
        except Exception as e:
            print(f"⚠️ Falha ao remover {arquivo}: {e}")
    print("✅ Finalizado.")

# ------------------------------------------------------------
# 🚀 Execução principal do script
# ------------------------------------------------------------

if __name__ == "__main__":
    if not PERFIL_ATIVO or not URL_ZIP or not PASTA_DADOS or not ARQUIVO_ALVO:
        print("❌ Perfil ativo ou configurações incompletas no JSON.")
    else:
        inicio = time.time()

        limpar_pasta_inicio(PASTA_DADOS)
        baixar_e_extrair_zip(URL_ZIP, PASTA_DADOS)
        caminho_planilha = os.path.join(PASTA_DADOS, ARQUIVO_ALVO)
        colunas_planilha = inspecionar_planilha(caminho_planilha)

        if atualizar_json:
            atualizar_dicionario_json(colunas_planilha)
        else:
            comparar_dicionario(colunas_planilha)

        limpar_arquivos_finais(PASTA_DADOS)
        print(f"\n✅ Script finalizado em {round(time.time() - inicio, 2)} segundos.")

