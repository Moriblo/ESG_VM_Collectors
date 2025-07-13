# ------------------------------------------------------------
# 🧠 Semântica MapBiomas — Inteligência para atribuição de significados
# ------------------------------------------------------------

import json
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# 🔧 Carregar configurações globais
# ------------------------------------------------------------

def carregar_config_global(caminho="setup.json"):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Erro ao carregar setup.json: {e}")
        return {}

# ------------------------------------------------------------
# 📘 Carregar cache local de definições
# ------------------------------------------------------------

def carregar_cache_local(caminho=None):
    cfg = carregar_config_global()
    caminho = caminho or cfg.get("cache_referencias_path", "referencias_mapbiomas.json")

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# ------------------------------------------------------------
# 🔍 Scraping leve do glossário MapBiomas
# ------------------------------------------------------------

def buscar_glossario_online(termo):
    cfg = carregar_config_global()
    url = cfg.get("url_glossario_oficial", "https://brasil.mapbiomas.org/glossario/")
    timeout = cfg.get("timeout_conexao", 10)

    try:
        res = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        itens = soup.find_all("div", class_="glossario-item")

        for item in itens:
            titulo = item.find("h3")
            texto = item.find("p")
            if titulo and texto and termo.lower() in titulo.text.lower():
                return texto.text.strip() + " 🧪 Definição extraída do glossário MapBiomas"
    except:
        pass

    return None

# ------------------------------------------------------------
# 📂 Atualizar cache com a legenda oficial
# ------------------------------------------------------------

def atualizar_cache_com_legenda():
    cfg = carregar_config_global()
    nome_csv = "mapbiomas-legend.csv"
    url = cfg.get("url_legenda_csv")
    caminho_cache = cfg.get("cache_referencias_path", "referencias_mapbiomas.json")
    timeout = cfg.get("timeout_conexao", 10)

    try:
        res = requests.get(url, timeout=timeout)
        with open(nome_csv, "wb") as f:
            f.write(res.content)

        df = pd.read_csv(nome_csv, encoding="utf-8")
        novos_significados = {}

        for _, row in df.iterrows():
            class_id = str(row.get("class_id", "")).strip()
            descricao = str(row.get("description", "")).strip()
            if class_id and descricao:
                novos_significados[class_id] = descricao + " 🧪 Definição da legenda oficial"

        if os.path.exists(caminho_cache):
            with open(caminho_cache, "r", encoding="utf-8") as f:
                cache = json.load(f)
        else:
            cache = {}

        cache.update(novos_significados)

        with open(caminho_cache, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

        print(f"✅ Cache atualizado com {len(novos_significados)} definições da legenda.")
    except Exception as e:
        print(f"⚠️ Erro ao processar legenda oficial: {e}")
    finally:
        if cfg.get("limpar_csv_legenda_apos_uso", True) and os.path.exists(nome_csv):
            os.remove(nome_csv)
            print("🧹 Arquivo CSV removido após uso.")

# ------------------------------------------------------------
# 🧠 Buscar definição de campo com múltiplas fontes
# ------------------------------------------------------------

def buscar_definicao(campo, cache_local):
    if campo in cache_local:
        return cache_local[campo]

    definicao_online = buscar_glossario_online(campo)
    if definicao_online:
        cache_local[campo] = definicao_online
        try:
            caminho_cache = carregar_config_global().get("cache_referencias_path", "referencias_mapbiomas.json")
            with open(caminho_cache, "w", encoding="utf-8") as f:
                json.dump(cache_local, f, indent=2, ensure_ascii=False)
        except:
            pass
        return definicao_online

    return "❓ Definir significado"
