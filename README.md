# ESG_VM_Collectors

Scripts para realizar: Extraction, Treatment e Loading (ETL) das fontes de dados para carregar nas tabelas definidas nos Datasets.

---

## 🗂️ Scripts coletores de ETL

| Fonte                 | Tabela Alvo | Script Python                                                                   | Status             |
|-----------------------|-------------|----------------------------------------------------------------------------------|--------------------|
| Naturebase.org        | GeoDados    | [etl_geodados_naturebase_scraper.py](./etl_geodados_naturebase_scraper.py)     | 🚧 em desenvolvimento |
| SICAR                 | GeoDados    | [etl_geodados_sicar.py](./etl_geodados_sicar.py)                               | 🚫 não iniciado    |
| Embrapa AgroAPI       | ProjetoNbS  | [etl_projetonbs_embrapa.py](./etl_projetonbs_embrapa.py)                       | 🚫 não iniciado    |
| B3 Sustentabilidade   | ProjetoNbS  | [etl_projetonbs_b3sustentabilidade.py](./etl_projetonbs_b3sustentabilidade.py) | 🚫 não iniciado    |
| ISE B3                | FundoESG    | [etl_fundoesg_iseb3.py](./etl_fundoesg_iseb3.py)                               | 🚫 não iniciado    |
| Ações Verdes          | FundoESG    | [etl_fundoesg_acoesverdes.py](./etl_fundoesg_acoesverdes.py)                   | 🚫 não iniciado    |
| Aliança Brasil NbS    | ProjetoNbS  | [etl_projetonbs_alianca.py](./etl_projetonbs_alianca.py)                       | 🚫 não iniciado    |
| MapBiomas             | GeoDados    | [etl_geodados_mapbiomas_scraper.py](./etl_geodados_mapbiomas_scraper.py)       | ⚠️ em testes       |
| GFW                   | GeoDados    | [etl_geodados_gfw_scraper.py](./etl_geodados_gfw_scraper.py)                   | 🚧 em desenvolvimento |
| OSM                   | GeoDados    | [etl_geodados_osm.py](./etl_geodados_osm.py)                                   | ⚠️ em testes       |

---

### 🔖 Legenda de status

- ✅ em produção
- ⚠️ em testes
- 🚧 em desenvolvimento
- ⏸️ on hold
- 🚫 não iniciado

---

## 🧩 Justificativa da nomenclatura

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

- Fonte: [naturebase-data (GitHub)](https://github.com/nature4climate/naturebase-data)
- Tipo de dado: áreas prioritárias para NbS
- Formato original: `.zip` contendo `.shp`
- Atributos principais: `biome`, `country`, `nbs_type`
- Tipo de coleta: scraping do GitHub

---

### 📊 Diagrama de Fluxo ETL

```text
[Scraping do repositório GitHub do Naturebase]
        ↓
[Download do shapefile .zip]
        ↓
[Extração dos arquivos]
        ↓
[Leitura e conversão para GeoDataFrame com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Empacotamento dos atributos em JSONB]
        ↓
[Inserção em tabela GeoDados]
        ↓
[Armazenamento do campo geometry como GEOMETRY(Geometry, 4326) via PostGIS]
```
