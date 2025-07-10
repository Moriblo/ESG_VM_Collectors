import os
import requests
import zipfile
import io
import geopandas as gpd
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 📥 [Download do shapefile da Geofabrik (OSM)]
# ------------------------------------------------------------

url = "https://download.geofabrik.de/south-america/brazil-latest-free.shp.zip"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
if res.status_code != 200:
    raise Exception(f"Erro ao baixar OSM: {res.status_code}")

destino = "dados/osm"
os.makedirs(destino, exist_ok=True)

with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(destino)

# ------------------------------------------------------------
# 📖 [Leitura do shapefile de estradas]
# ------------------------------------------------------------

shp_path = os.path.join(destino, "gis_osm_roads_free_1.shp")
if not os.path.exists(shp_path):
    raise Exception("Arquivo gis_osm_roads_free_1.shp não encontrado.")

gdf = gpd.read_file(shp_path)

# ------------------------------------------------------------
# 🌐 [Conversão de CRS para EPSG:4326 (WGS84)]
# ------------------------------------------------------------

gdf = gdf.to_crs(epsg=4326)

# ------------------------------------------------------------
# 🧹 [Empacotar atributos em JSONB]
# ------------------------------------------------------------

gdf = gdf[gdf.is_valid]
gdf["fonte"] = "osm"
gdf["atributos"] = gdf.drop(columns=["geometry"]).apply(lambda row: row.to_dict(), axis=1)
gdf = gdf[["fonte", "atributos", "geometry"]]

# ------------------------------------------------------------
# 🗃️ [Inserção em tabela GeoDados]
# ------------------------------------------------------------

engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")
gdf.to_postgis("geodados", engine, if_exists="append", index=False)

print("✅ Dados do OSM inseridos com sucesso.")
