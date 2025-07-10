# ESG_VM_Collectors
---
### 🗂️ Padrão sugerido para os scripts de ETL

| Fonte                     | Tabela Alvo   | Nome do Script Sugerido                  |
|--------------------------|---------------|------------------------------------------|
| SICAR                    | GeoDados      | etl_geodados_sicar.py                   |
| Embrapa AgroAPI          | ProjetoNbS    | etl_projetonbs_embrapa.py               |
| B3 Sustentabilidade      | ProjetoNbS    | etl_projetonbs_b3sustentabilidade.py    |
| ISE B3 / Ações Verdes    | FundoESG      | etl_fundoesg_b3.py                      |
| Aliança Brasil NbS       | ProjetoNbS    | etl_projetonbs_alianca.py               |
| MapBiomas / GFW / OSM    | GeoDados      | etl_geodados_mapbiomas_gfw_osm.py       |

### 🧩 Justificativa da nomenclatura

| Parte do nome   | Significado                                                                 |
|------------------|------------------------------------------------------------------------------|
| `etl_`           | Prefixo padrão para scripts de Extração, Transformação e Carga              |
| `geodados_`      | Indica a tabela de destino no modelo ER                                     |
| `naturebase`     | Nome da fonte de dados (específico e descritivo)                            |
| `.py`            | Extensão do script Python                                                   |

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
