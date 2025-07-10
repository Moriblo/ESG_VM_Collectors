import os
import requests
import zipfile
import io
import geopandas as gpd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 🌐 [Acessar página de downloads do MapBiomas]
# ------------------------------------------------------------

url = "https://brasil.mapbiomas.org/downloads"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao acessar página do MapBiomas: {res.status_code}")

# ------------------------------------------------------------
# 🔍 [Extrair links de shapefiles da página]
# ------------------------------------------------------------

soup = BeautifulSoup(res.text, "html.parser")
links = soup.find_all("a", href=True)

# Filtrar links para arquivos .zip de uso do solo
shapefile_links = [a["href"] for a in links if ".zip" in a["href"].lower() and "uso" in a["href"].lower()]

if not shapefile_links:
    raise Exception("Nenhum link de shapefile de uso do solo encontrado.")

# Usar o primeiro link encontrado (pode ser ajustado para lógica mais refinada)
download_url = shapefile_links[0]
print(f"🔗 Baixando shapefile do MapBiomas: {download_url}")

# ------------------------------------------------------------
# 📥 [Download e extração do shapefile]
# ------------------------------------------------------------

res = requests.get(download_url, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao baixar shapefile: {res.status_code}")

destino = "dados/mapbiomas"
os.makedirs(destino, exist_ok=True)

with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(destino)

# ------------------------------------------------------------
# 📖 [Leitura e conversão para GeoDataFrame com GeoPandas]
# ------------------------------------------------------------

print("📚 Lendo shapefile com GeoPandas...")

# Procurar o primeiro .shp extraído
shapefiles = [f for f in os.listdir(destino) if f.endswith(".shp")]
if not shapefiles:
    raise Exception("Nenhum arquivo .shp encontrado após extração.")

shp_path = os.path.join(destino, shapefiles[0])
gdf = gpd.read_file(shp_path)

# ------------------------------------------------------------
# 🌐 [Conversão de CRS para EPSG:4326 (WGS84)]
# ------------------------------------------------------------

print("🌍 Convertendo CRS para EPSG:4326...")
gdf = gdf.to_crs(epsg=4326)

# ------------------------------------------------------------
# 🧹 [Enriquecimento: empacotar atributos em JSONB]
# ------------------------------------------------------------

gdf = gdf[gdf.is_valid]
gdf["fonte"] = "mapbiomas"
gdf["atributos"] = gdf.drop(columns=["geometry"]).apply(lambda row: row.to_dict(), axis=1)
gdf = gdf[["fonte", "atributos", "geometry"]]

# ------------------------------------------------------------
# 🗃️ [Inserção em tabela GeoDados]
# ------------------------------------------------------------

engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")

print("📤 Inserindo dados na tabela 'geodados'...")
gdf.to_postgis("geodados", engine, if_exists="append", index=False)

print("✅ Dados do MapBiomas inseridos com sucesso.")
