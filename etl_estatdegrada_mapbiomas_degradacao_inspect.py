import os
import requests
import zipfile
import io
import pandas as pd

# Este comentário é só um teste...
# -------------------- Configurações --------------------

URL_ZIP = "https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_8/degradation/statistics/brazil-degradation-statistics.zip"
PASTA_DADOS = "dados/mapbiomas_degradacao"
CAMPOS_INTERESSANTES = [
    "estado", "bioma", "municipio", "id_municipio_ibge",
    "categoria_degradacao", "area_ha", "ano"
]

# -------------------- Baixar e extrair --------------------

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(URL_ZIP, headers=headers)
if res.status_code != 200:
    raise Exception(f"Falha ao baixar ZIP: {res.status_code}")

os.makedirs(PASTA_DADOS, exist_ok=True)
with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(PASTA_DADOS)

# -------------------- Explorar arquivos e abas --------------------

arquivos = [f for f in os.listdir(PASTA_DADOS) if f.endswith(".xlsx")]

for arquivo in arquivos:
    caminho = os.path.join(PASTA_DADOS, arquivo)
    print(f"\n📁 Arquivo: {arquivo}")
    try:
        planilhas = pd.ExcelFile(caminho).sheet_names
        for aba in planilhas:
            print(f"  └─ 📝 Aba: {aba}")
            try:
                df = pd.read_excel(caminho, sheet_name=aba, nrows=5, engine="openpyxl")
                colunas = df.columns.str.lower().str.strip()
                print(f"       📊 Colunas: {list(colunas)}")

                encontrados = [c for c in CAMPOS_INTERESSANTES if c in colunas]
                if encontrados:
                    print(f"       ✅ Campos encontrados: {encontrados}")
                else:
                    print(f"       ❌ Nenhum campo relevante detectado")

            except Exception as e:
                print(f"       ⚠️ Erro ao ler aba: {e}")
    except Exception as e:
        print(f"  ⚠️ Falha ao acessar abas → {e}")

