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
    """
    Busca uma definição aproximada no glossário oficial do MapBiomas.
    Usa correspondência exata e fuzzy matching.
    Retorna a descrição ou None se não encontrada.
    """
    url = "https://brasil.mapbiomas.org/glossario"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        itens = soup.find_all("div", class_="glossario-item")
        print(f"\n📚 Glossário contém {len(itens)} entradas.")

        termo_normalizado = termo.strip().lower().replace("_", " ")

        candidatos = {}
        titulos_disponiveis = []

        for item in itens:
            titulo = item.find("h3")
            descricao = item.find("p")
            if titulo and descricao:
                titulo_texto = titulo.text.strip().lower()
                titulos_disponiveis.append(titulo_texto)

                # 🧮 Similaridade entre termo buscado e título
                ratio = difflib.SequenceMatcher(None, termo_normalizado, titulo_texto).ratio()
                if termo_normalizado in titulo_texto or titulo_texto in termo_normalizado or ratio > 0.6:
                    candidatos[titulo_texto] = descricao.text.strip()

        if candidatos:
            melhor = sorted(candidatos.items(), key=lambda x: difflib.SequenceMatcher(None, termo_normalizado, x[0]).ratio(), reverse=True)[0]
            print(f"✅ Definição encontrada por aproximação: {melhor[0]}")
            return melhor[1]

        print(f"⚠️ Nenhuma definição aproximada encontrada para '{termo}'.")
        print("📘 Exemplos disponíveis no glossário:")
        for titulo in titulos_disponiveis[:10]:
            print(f"   • {titulo}")
        return None

    except Exception as e:
        print(f"❌ Erro ao acessar o glossário online: {e}")
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

# ------------------------------------------------------------
# 📘 Gerar sugestões semânticas para campos não definidos no cache
# ------------------------------------------------------------

def gerar_sugestoes_semanticas(colunas_detectadas, referencias, salvar_arquivo=True, caminho_arquivo="sugestoes_semantica.jsonc"):
    """
    Identifica campos detectados na planilha que não possuem definição no cache
    e gera sugestões de significado em formato JSONC (comentado), pronto para inclusão manual.
    """

    print("\n📘 Gerando sugestões semânticas para campos não definidos...")

    # 🔎 Verificar quais campos não estão definidos no cache
    candidatos = []
    for col in colunas_detectadas:
        if col.isdigit() and 1980 <= int(col) <= 2100:
            continue
        chave = col.strip().lower().replace(" ", "_")
        if chave not in referencias:
            candidatos.append(col)

    if not candidatos:
        print("✅ Todos os campos já possuem definição no cache.")
        return

    print(f"⚠️ Encontrados {len(candidatos)} campos sem definição:")
    for campo in candidatos:
        print(f"   • {campo}")

    # 🧠 Gerar sugestões com comentários técnicos
    sugestoes = []
    for campo in candidatos:
        chave = campo.strip().lower().replace(" ", "_")

        if chave == "name":
            comentario = "Nome da entidade espacial representada pela feição (ex: estado, município, bioma)."
            definicao = "Nome descritivo da feição espacial representada na planilha."
        elif chave == "index":
            comentario = "Indicador técnico calculado com base em séries temporais ou parâmetros ambientais."
            definicao = "Indicador ou métrica associada à feição, como índice de degradação ou frequência."
        else:
            comentario = f"Definição técnica para o campo '{campo}' ainda não incluída no cache."
            definicao = "❓ Definir significado"

        sugestoes.append({
            "campo": campo,
            "comentario": comentario,
            "definicao": definicao
        })

    # 📦 Montar bloco JSONC comentado
    bloco_jsonc = "// 🔍 Sugestões de definições semânticas\n{\n"
    for s in sugestoes:
        bloco_jsonc += f'  // {s["campo"]}: {s["comentario"]}\n'
        bloco_jsonc += f'  "{s["campo"]}": "{s["definicao"]}",\n'
    bloco_jsonc = bloco_jsonc.rstrip(",\n") + "\n}"

    print("\n📦 Bloco JSON sugerido:\n")
    print(bloco_jsonc)

    # 💾 Salvar como arquivo auxiliar, se habilitado
    if salvar_arquivo:
        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(bloco_jsonc)
            print(f"\n✅ Sugestões salvas em: {caminho_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo de sugestões: {e}")
