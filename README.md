# ESG_VM_Collectors
---
## 🔁 ETL: [Naturebase.org](https://naturebase.org) → GeoDados

> Esta construção corresponde à linha da tabela em [Datasets/Mapeamento: Fontes Open Free → Tabelas do Projeto](https://github.com/Moriblo/ESG_VM_Datasets)
> **Objetivo:** importar áreas prioritárias para NbS (Soluções baseadas na Natureza), com atributos como bioma, país e tipo de NbS.

---

### 📦 O que estamos baixando?

Do site [Naturebase.org](https://naturebase.org), baixamos arquivos geoespaciais contendo:
- **Shapefiles** ou **GeoTIFFs** com polígonos de áreas prioritárias
- Atributos como: `biome`, `country`, `nbs_type`
- Formato original: `.shp`, `.tif`, `.geojson` (dependendo da camada)

---

### 📊 Diagrama de Fluxo ETL

```text
[Download manual do shapefile do Naturebase.org]
        ↓
[Arquivo: naturebase_areas_prioritarias.shp]
        ↓
[Leitura e conversão para GeoDataFrame com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Enriquecimento: renomear colunas, validar geometria]
        ↓
[Inserção em tabela GeoDados (PostGIS)]

