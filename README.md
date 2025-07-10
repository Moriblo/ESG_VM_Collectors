# ESG_VM_Collectors
- Scripts para realizar: Extraction, Treatment e Loading (ETL) das fontes de dados para carregar nas tabelas definidas nos Datasets.

## 🗂️ Scripts coletores de ETL

| Fonte                 | Tabela Alvo | Script Python                                                                 | Status         |
|-----------------------|-------------|-------------------------------------------------------------------------------|----------------|
| Naturebase.org        | GeoDados    | [etl_geodados_naturebase.py](./etl_geodados_naturebase.py)                   | ⏸️ on hold     |
| SICAR                 | GeoDados    | [etl_geodados_sicar.py](./etl_geodados_sicar.py)                             | 🚫 não iniciado|
| Embrapa AgroAPI       | ProjetoNbS  | [etl_projetonbs_embrapa.py](./etl_projetonbs_embrapa.py)                     | 🚫 não iniciado|
| B3 Sustentabilidade   | ProjetoNbS  | [etl_projetonbs_b3sustentabilidade.py](./etl_projetonbs_b3sustentabilidade.py)| 🚫 não iniciado|
| ISE B3                | FundoESG    | [etl_fundoesg_iseb3.py](./etl_fundoesg_iseb3.py)                             | 🚫 não iniciado|
| Ações Verdes          | FundoESG    | [etl_fundoesg_acoesverdes.py](./etl_fundoesg_acoesverdes.py)                 | 🚫 não iniciado|
| Aliança Brasil NbS    | ProjetoNbS  | [etl_projetonbs_alianca.py](./etl_projetonbs_alianca.py)                     | 🚫 não iniciado|
| MapBiomas             | GeoDados    | [etl_geodados_mapbiomas_scraper.py](./etl_geodados_mapbiomas_scraper.py)     | ⚠️ em testes   |
| GFW + OSM             | GeoDados    | [etl_geodados_gfw_osm.py](./etl_geodados_gfw_osm.py)                         | ⚠️ em testes   |

---

### 🔖 Legenda de status

- ✅ em produção
- ⚠️ em testes
- 🚧 em desenvolvimento
- ⏸️ on hold
- 🚫 não iniciado

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
## 🔁 ETL: MapBiomas / GFW / OSM → GeoDados (modularizado)

- Esta construção corresponde às linhas da tabela em [Datasets/Mapeamento: Fontes Open Free → Tabelas do Projeto](https://github.com/Moriblo/ESG_VM_Datasets)
- **Objetivo:** importar dados geoespaciais de uso do solo, alertas ambientais e infraestrutura para compor a base `GeoDados`, com estrutura genérica e extensível.
---
### 📦 Fontes e scripts separados

| Fonte       | Script Python                      | Tipo de Coleta       |
|-------------|-------------------------------------|-----------------------|
| MapBiomas   | `etl_geodados_mapbiomas_scraper.py` | Webscraping + ETL     |
| GFW + OSM   | `etl_geodados_gfw_osm.py`           | Download direto + ETL |

### 📊 Diagrama de Fluxo ETL (comum aos dois scripts)

```text
[Coleta dos dados (download direto ou scraping)]
        ↓
[Extração dos arquivos .zip ou leitura direta]
        ↓
[Leitura e conversão para GeoDataFrame com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Enriquecimento: empacotar atributos em JSONB]
        ↓
[Inserção em tabela GeoDados]
        ↓
[Armazenamento do campo geometry como GEOMETRY(Geometry, 4326) via PostGIS]
```

