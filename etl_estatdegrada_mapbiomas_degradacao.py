import os
import requests
import zipfile
import io
import pandas as pd
from sqlalchemy import create_engine

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
# 📖 Leitura segura das planilhas
# ------------------------------------------------------------

arquivos = [f for f in os.listdir(pasta_dados) if f.endswith(".xlsx")]
df_final = pd.DataFrame()

for arquivo in arquivos:
    caminho = os.path.join(pasta_dados, arquivo)
    print(f"\n📂 Processando arquivo: {arquivo}")

    try:
        planilhas = pd.ExcelFile(caminho).sheet_names
    except Exception as e:
        print(f"⚠️ Falha ao ler estrutura do arquivo {arquivo} → {e}")
        continue

    for aba in planilhas:
        print(f"  📄 Lendo aba: {aba}")
        try:
            df = pd.read_excel(caminho, sheet_name=aba, nrows=500)  # limite de linhas para teste
            df["fonte"] = "mapbiomas_degradacao"
            df["arquivo_origem"] = arquivo
            df["planilha_origem"] = aba
            df_final = pd.concat([df_final, df], ignore_index=True)
        except Exception as e:
            print(f"    ⚠️ Erro ao ler aba '{aba}': {e}")
            continue

# ------------------------------------------------------------
# 🗃️ Inserção segura em banco de dados
# ------------------------------------------------------------

if df_final.empty:
    print("⚠️ Nenhum dado foi carregado. Interrompendo carga.")
else:
    engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")
    try:
        df_final.to_sql("estatdegrada", engine, if_exists="append", index=False)
        print(f"\n✅ Inserção concluída com {len(df_final)} registros.")
    except Exception as e:
        print(f"❌ Falha ao inserir dados no banco: {e}")
