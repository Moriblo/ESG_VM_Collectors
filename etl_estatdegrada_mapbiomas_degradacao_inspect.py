import os
import requests
import zipfile
import io
import pandas as pd

# ------------------------------------------------------------
# 🌐 Download do ZIP de estatísticas
# ------------------------------------------------------------

url_zip = "https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_8/degradation/statistics/brazil-degradation-statistics.zip"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url_zip, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao baixar estatísticas: {res.status_code}")

pasta_dados = "dados/mapbiomas_degradacao"
os.makedirs(pasta_dados, exist_ok=True)

with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(pasta_dados)

# ------------------------------------------------------------
# 📋 Listar arquivos .xlsx e suas abas
# ------------------------------------------------------------

arquivos = [f for f in os.listdir(pasta_dados) if f.endswith(".xlsx")]

print("\n📁 Arquivos encontrados e suas respectivas abas:\n")

for i, arquivo in enumerate(arquivos, start=1):
    caminho = os.path.join(pasta_dados, arquivo)
    print(f"{i:02d}. 📂 Arquivo: {arquivo}")
    try:
        planilhas = pd.ExcelFile(caminho).sheet_names
        for aba in planilhas:
            print(f"     └─ 📄 Aba: {aba}")
    except Exception as e:
        print(f"     ❌ Erro ao acessar abas: {e}")
    print()

print("\n✅ Listagem concluída. Nenhum dado foi carregado ainda.")
