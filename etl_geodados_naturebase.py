import requests
import zipfile
import io
import os
import geopandas as gpd
from sqlalchemy import create_engine

# ------------------------------------------------------------
# 📥 [Download automático do shapefile do repositório Naturebase]
# ------------------------------------------------------------

# URL do shapefile compactado (exemplo: áreas prioritárias globais)
url = "https://github.com/nature4climate/naturebase-data/raw/main/data/global/NbS_Priority_Areas_Global_Shapefile.zip"

# Pasta de destino para extração
destino = "dados/naturebase"
os.makedirs(destino, exist_ok=True)

print("🔽 Baixando shapefile do Naturebase...")
res = requests.get(url)
with zipfile.ZipFile(io.BytesIO(res.content)) as z:
    z.extractall(destino)
print("✅ Download e extração concluídos.")

# ------------------------------------------------------------
# 📂 [Arquivo: NbS_Priority_Areas_Global_Shapefile.zip]
# ------------------------------------------------------------

# Caminho para o shapefile extraído
shapefile_path = os.path.join(destino, "NbS_Priority_Areas_Global.shp")

# ------------------------------------------------------------
# 📖 [Leitura e conversão para GeoDataFrame com GeoPandas]
# ------------------------------------------------------------

print("📚 Lendo shapefile com GeoPandas...")
gdf = gpd.read_file(shapefile_path)

# ------------------------------------------------------------
# 🌐 [Conversão de CRS para EPSG:4326 (WGS84)]
# ------------------------------------------------------------

print("🌍 Convertendo CRS para EPSG:4326...")
gdf = gdf.to_crs(epsg=4326)

# ------------------------------------------------------------
# 🧹 [Enriquecimento: renomear colunas, validar geometria]
# ------------------------------------------------------------

# Selecionar e renomear colunas relevantes
# (ajuste os nomes conforme os campos reais do shapefile)
gdf = gdf[["geometry", "BIOME", "COUNTRY", "NBS_TYPE"]]
gdf.columns = ["geometry", "bioma", "pais", "tipo"]

# Validar geometrias (remover inválidas, se necessário)
gdf = gdf[gdf.is_valid]

# Adicionar coluna de tipo de dado (opcional)
gdf["fonte"] = "Naturebase.org"

# ------------------------------------------------------------
# 🗃️ [Inserção em tabela GeoDados]
# ------------------------------------------------------------

# Conectar ao banco PostgreSQL com extensão PostGIS
engine = create_engine("postgresql://usuario:senha@localhost:5432/seubanco")

# ------------------------------------------------------------
# 🧭 [Armazenamento do campo poligono como geometry(Polygon, 4326) via PostGIS]
# ------------------------------------------------------------

print("📤 Inserindo dados na tabela 'geodados'...")
gdf.to_postgis("geodados", engine, if_exists="append", index=False)
print("✅ Dados inseridos com sucesso.")
