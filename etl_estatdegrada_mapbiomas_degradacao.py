import os
import requests
import zipfile
import io
import pandas as pd
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 🔧 DEFINA SUA CONEXÃO COM O BANCO
# ------------------------------------------------------------

# ⚠️ Substitua pelas credenciais reais
USUARIO_DB = "postgres"
SENHA_DB = "Isabella&01"
HOST_DB = "localhost"
PORTA_DB = "5432"
NOME_DB = "esg_vm_core"

engine = create_engine(f"postgresql://{USUARIO_DB}:{SENHA_DB}@{HOST_DB}:{PORTA_DB}/{NOME_DB}")

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
# 🧼 Função para tratar encoding de texto
# ------------------------------------------------------------

def forcar_utf8(df):
    for col in df.select_dtypes(include=["object"]):
        df[col] = df[col].astype(str).apply(
            lambda x: x.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
        )
    return df

# ------------------------------------------------------------
# 📖 Leitura das planilhas com tratamento
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
            df = pd.read_excel(caminho, sheet_name=aba, nrows=500, engine='openpyxl')
            df = forcar_utf8(df)

            df["fonte"] = "mapbiomas_degradacao"
            df["arquivo_origem"] = arquivo
            df["planilha_origem"] = aba
            df_final = pd.concat([df_final, df], ignore_index=True)
        except Exception as e:
            print(f"    ⚠️ Erro ao ler aba '{aba}': {e}")
            continue

# ------------------------------------------------------------
# 🗃️ Inserção segura no banco
# ------------------------------------------------------------

if df_final.empty:
    print("⚠️ Nenhum dado foi carregado. Interrompendo carga.")
else:
    try:
        df_final = forcar_utf8(df_final)
        df_final.to_sql("estatdegrada", engine, if_exists="append", index=False, method="multi")
        print(f"\n✅ Inserção concluída com {len(df_final)} registros.")
    except Exception as e:
        print(f"❌ Falha ao inserir dados no banco: {e}")
