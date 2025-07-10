import requests
from bs4 import BeautifulSoup

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
shapefile_links = [a["href"] for a in links if ".zip" in a["href"] and "uso" in a["href"].lower()]

for link in shapefile_links:
    print(f"🔗 Link encontrado: {link}")
