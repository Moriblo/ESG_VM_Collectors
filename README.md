# ESG_VM_Collectors
---
## 🔁 ETL: Naturebase.org → GeoDados

> Esta construção corresponde à linha da tabela anexa:
> 🌍 Naturebase.org → `GeoDados` — Áreas prioritárias para NbS (polígonos, biomas, países)

### 📊 Diagrama de Fluxo

```text
[Download manual ou via script]
        ↓
[Shapefile / GeoTIFF / GeoJSON]
        ↓
[Conversão para GeoJSON com GeoPandas]
        ↓
[Enriquecimento: bioma, país, tipo]
        ↓
[Validação de geometria e CRS (EPSG:4326)]
        ↓
[Inserção em tabela GeoDados (PostGIS)]
