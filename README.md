# ESG_VM_Collectors
- Scripts para realizar: Extraction, Treatment e Loading (ETL) das fontes de dados para carregar nas tabelas definidas nos Datasets.
---
---
## 🗂️ Padrão sugerido para os scripts de ETL

| Fonte                     | Tabela Alvo   | Nome do Script Sugerido                  |
|--------------------------|---------------|------------------------------------------|
| Naturebase.org           | GeoDados      | etl_geodados_naturebase.py              |
| SICAR                    | GeoDados      | etl_geodados_sicar.py                   |
| Embrapa AgroAPI          | ProjetoNbS    | etl_projetonbs_embrapa.py               |
| B3 Sustentabilidade      | ProjetoNbS    | etl_projetonbs_b3sustentabilidade.py    |
| ISE B3                   | FundoESG      | etl_fundoesg_iseb3.py                   |
| Ações Verdes             | FundoESG      | etl_fundoesg_acoesverdes.py             |
| Aliança Brasil NbS       | ProjetoNbS    | etl_projetonbs_alianca.py               |
| MapBiomas                | GeoDados      | etl_geodados_mapbiomas.py               |
| GFW                      | GeoDados      | etl_geodados_gfw.py                     |
| OSM                      | GeoDados      | etl_geodados_osm.py                     |


## 🧩 Justificativa da nomenclatura

| Parte do nome   | Significado                                                                 |
|------------------|------------------------------------------------------------------------------|
| `etl_`           | Prefixo padrão para scripts de Extração, Transformação e Carga              |
| `geodados_`      | Indica a tabela de destino no modelo ER                                     |
| `naturebase`     | Nome da fonte de dados (específico e descritivo)                            |
| `.py`            | Extensão do script Python                                                   |

---
---
## 🔁 ETL: [Naturebase.org](https://naturebase.org) → GeoDados

- Esta construção corresponde à linha da tabela em [Datasets/Mapeamento: Fontes Open Free → Tabelas do Projeto](https://github.com/Moriblo/ESG_VM_Datasets)
- **Objetivo:** importar áreas prioritárias para NbS (Soluções baseadas na Natureza), com atributos como bioma, país e tipo de NbS.
---
### 📦 O que estamos baixando?
- Do site [Naturebase.org](https://naturebase.org), baixamos arquivos geoespaciais contendo:
  - **Shapefiles** ou **GeoTIFFs** com polígonos de áreas prioritárias
  - Atributos como: `biome`, `country`, `nbs_type`
  - Formato original: `.shp`, `.tif`, `.geojson` (dependendo da camada)
  - Fonte oficial de dados: [naturebase-data (GitHub)](https://github.com/nature4climate/naturebase-data)
---
### 📊 Diagrama de Fluxo ETL
```text
[Download automático do shapefile do repositório Naturebase]
        ↓
[Arquivo: NbS_Priority_Areas_Global_Shapefile.zip]
        ↓
[Leitura e conversão para GeoDataFrame com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Enriquecimento: renomear colunas, validar geometria]
        ↓
[Inserção em tabela GeoDados]
        ↓
[Armazenamento do campo poligono como geometry(Polygon, 4326) via PostGIS]
````
---
### 🔁 Comparativo: Naturebase.org vs. MapBiomas / GFW / OSM

| Critério                         | Naturebase.org                               | MapBiomas / GFW / OSM                          |
|----------------------------------|----------------------------------------------|------------------------------------------------|
| Tipo de dado                     | Áreas prioritárias para NbS                  | Uso do solo, alertas, infraestrutura           |
| Formato                          | .shp, .tif, .geojson                         | .tif, .shp, .osm, .geojson                     |
| Acesso automático                | ❌ (interface manual)                        | ✅ (links diretos, APIs, scraping viável)      |
| Frequência de atualização        | Estática                                     | Regular (anual ou mensal, dependendo da fonte) |
| Cobertura geográfica             | Global                                       | Brasil (MapBiomas), Global (GFW, OSM)          |
| Potencial para ETL automatizado | Baixo                                        | Alto                                           |

---
---
## 🔁 ETL: MapBiomas / GFW / OSM → GeoDados

- Esta construção corresponde à linha da tabela em [Datasets/Mapeamento: Fontes Open Free → Tabelas do Projeto](https://github.com/Moriblo/ESG_VM_Datasets)
- **Objetivo:** importar dados geoespaciais de uso do solo, alertas ambientais e infraestrutura para compor a base `GeoDados`.

---

### 📦 O que estamos baixando?

- **MapBiomas**: uso e cobertura da terra (coleção 7, ano 2022)
  - Fonte: [https://mapbiomas.org](https://mapbiomas.org)
  - Formato: `.shp` (uso_solo_2022.zip)
- **GFW (Global Forest Watch)**: alertas de desmatamento (Landsat)
  - Fonte: [https://data.globalforestwatch.org](https://data.globalforestwatch.org)
  - Formato: `.shp` (umd_landsat_alerts.zip)
- **OpenStreetMap (Geofabrik)**: infraestrutura (estradas, ferrovias, etc.)
  - Fonte: [https://download.geofabrik.de](https://download.geofabrik.de)
  - Formato: `.shp` (brazil-latest-free.shp.zip)

---

### 📊 Diagrama de Fluxo ETL

```text
[Download automático dos shapefiles das fontes MapBiomas, GFW e OSM]
        ↓
[Arquivos: uso_solo_mapbiomas.zip, alertas_gfw.zip, infraestrutura_osm.shp]
        ↓
[Leitura e conversão para GeoDataFrame com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Enriquecimento: padronizar colunas, validar geometria, empacotar atributos em JSONB]
        ↓
[Inserção em tabela GeoDados]
        ↓
[Armazenamento do campo geometry como GEOMETRY(Geometry, 4326) via PostGIS]
````

