import os
import geopandas as gpd
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 📁 Configuração: pastas com shapefiles organizados por UF
# ------------------------------------------------------------

PASTA_BASE = "dados/sicar/uf"
engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")

# ------------------------------------------------------------
# 🔁 Itera por estado e processa shapefiles
# ------------------------------------------------------------

for uf in os.listdir(PASTA_BASE):
    caminho_uf = os.path.join(PASTA_BASE, uf)
    if not os.path.isdir(caminho_uf):
        continue

    for arquivo in os.listdir(caminho_uf):
        if not arquivo.endswith(".shp"):
            continue

        caminho_shp = os.path.join(caminho_uf, arquivo)
        print(f"🗺️ Processando {caminho_shp}")

        gdf = gpd.read_file(caminho_shp)
        gdf = gdf.to_crs(epsg=4326)
        gdf = gdf[gdf.is_valid]

        gdf["fonte"] = "sicar"
        gdf["atributos"] = gdf.drop(columns=["geometry"]).apply(lambda row: row.to_dict(), axis=1)
        gdf = gdf[["fonte", "atributos", "geometry"]]

        gdf.to_postgis("geodados", engine, if_exists="append", index=False)
        print(f"✅ Inserido no banco: {arquivo}")
