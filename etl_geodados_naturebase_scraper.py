import os
import requests
import zipfile
import io
import geopandas as gpd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 🌐 [Acessar repositório GitHub do Naturebase]
# ------------------------------------------------------------

repo_url = "https://github.com/nature4climate/naturebase-data/tree/main/data/shapefiles"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(repo_url, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao acessar repositório do Naturebase: {res.status_code}")

# ------------------------------------------------------------
# 🔍 [Scraping do link de download do shapefile .zip]
# ------------------------------------------------------------

soup = BeautifulSoup(res.text, "html.parser")
links = soup.find_all("a", href=True)

zip_links = [
    "https://github.com" + a["href"].replace("/blob", "").replace("main", "raw/main")
    for a in links if a["href"].endswith(".zip")
]

if not zip_links:
    raise Exception("Nenhum link .zip encontrado no repositório.")

download_url = zip_links[0]
print(f"🔗 Baixando shapefile do Naturebase: {download_url}")

# ------------------------------------------------------------
# 📥 [Download e extração do shapefile]
# ------------------------------------------------------------

res = requests.get(download_url, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao baixar shapefile: {res.status_code}")

destino = "dados/naturebase"
os.makedirs(destino, exist_ok=True)

with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(destino)

# ------------------------------------------------------------
# 📖 [Leitura do shapefile]
# ------------------------------------------------------------

shapefiles = [f for f in os.listdir(destino) if f.endswith(".shp")]
if not shapefiles:
    raise Exception("Nenhum arquivo .shp encontrado após extração.")

shp_path = os.path.join(destino, shapefiles[0])
gdf = gpd.read_file(shp_path)

# ------------------------------------------------------------
# 🌐 [Conversão de CRS para EPSG:4326]
# ------------------------------------------------------------

gdf = gdf.to_crs(epsg=4326)

# ------------------------------------------------------------
# 🧹 [Empacotar atributos em JSONB]
# ------------------------------------------------------------

gdf = gdf[gdf.is_valid]
gdf["fonte"] = "naturebase"
gdf["atributos"] = gdf.drop(columns=["geometry"]).apply(lambda row: row.to_dict(), axis=1)
gdf = gdf[["fonte", "atributos", "geometry"]]

# ------------------------------------------------------------
# 🗃️ [Inserção em tabela GeoDados]
# ------------------------------------------------------------

engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")
gdf.to_postgis("geodados", engine, if_exists="append", index=False)

print("✅ Dados do Naturebase inseridos com sucesso.")
