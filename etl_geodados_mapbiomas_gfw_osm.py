import os
import requests
import zipfile
import io
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from shapely.geometry import mapping

# ------------------------------------------------------------
# 📥 [Download automático dos shapefiles das fontes MapBiomas, GFW e OSM]
# ------------------------------------------------------------


urls = {
    "gfw": "https://data.globalforestwatch.org/download/alerts/umd_landsat_alerts.zip",
    "osm": "https://download.geofabrik.de/south-america/brazil-latest-free.shp.zip"
}


destino = "dados/fontes_geodados"
os.makedirs(destino, exist_ok=True)

arquivos_extraidos = {}

for fonte, url in urls.items():
    print(f"🔽 Baixando dados de {fonte}...")
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"Erro ao baixar {fonte}: {res.status_code}")
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        z.extractall(os.path.join(destino, fonte))
        arquivos_extraidos[fonte] = os.path.join(destino, fonte)

# ------------------------------------------------------------
# 📖 [Leitura e conversão para GeoDataFrame com GeoPandas]
# ------------------------------------------------------------

print("📚 Lendo shapefiles com GeoPandas...")

# Ajuste os nomes conforme os arquivos reais extraídos
mapbiomas_shp = os.path.join(arquivos_extraidos["mapbiomas"], "uso_solo_2022.shp")
gfw_shp = os.path.join(arquivos_extraidos["gfw"], "umd_landsat_alerts.shp")
osm_shp = os.path.join(arquivos_extraidos["osm"], "gis_osm_roads_free_1.shp")

gdf_mapbiomas = gpd.read_file(mapbiomas_shp)
gdf_gfw = gpd.read_file(gfw_shp)
gdf_osm = gpd.read_file(osm_shp)

# ------------------------------------------------------------
# 🌐 [Conversão de CRS para EPSG:4326 (WGS84)]
# ------------------------------------------------------------

print("🌍 Convertendo CRS para EPSG:4326...")
gdf_mapbiomas = gdf_mapbiomas.to_crs(epsg=4326)
gdf_gfw = gdf_gfw.to_crs(epsg=4326)
gdf_osm = gdf_osm.to_crs(epsg=4326)

# ------------------------------------------------------------
# 🧹 [Enriquecimento: padronizar colunas, validar geometria, adicionar metadados]
# ------------------------------------------------------------

def preparar_gdf(gdf, fonte):
    gdf = gdf[gdf.is_valid]
    gdf["fonte"] = fonte
    gdf["atributos"] = gdf.drop(columns=["geometry"]).apply(lambda row: row.to_dict(), axis=1)
    return gdf[["fonte", "atributos", "geometry"]]

gdf_mapbiomas = preparar_gdf(gdf_mapbiomas, "mapbiomas")
gdf_gfw = preparar_gdf(gdf_gfw, "gfw")
gdf_osm = preparar_gdf(gdf_osm, "osm")

# ------------------------------------------------------------
# 🗃️ [Inserção em tabela GeoDados com JSONB + Geometry]
# ------------------------------------------------------------

engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")

print("📤 Inserindo dados na tabela 'geodados'...")

for gdf in [gdf_mapbiomas, gdf_gfw, gdf_osm]:
    gdf.to_postgis("geodados", engine, if_exists="append", index=False)

print("✅ Dados inseridos com sucesso.")
