# Diagrama ETL — Naturebase.org

> Este documento descreve o fluxo de Extração, Transformação e Carga (ETL) do coletor [`etl_geodados_naturebase_scraper.py`](./etl_geodados_naturebase_scraper.py), responsável por importar dados da fonte **Naturebase.org** para a tabela `GeoDados`.

---

## 🎯 Objetivo

Importar áreas prioritárias para NbS (Soluções baseadas na Natureza), com atributos como `biome`, `country` e `nbs_type`, e armazená-las na tabela `GeoDados` com estrutura genérica baseada em `JSONB` e `GEOMETRY`.

---

## 📦 Fonte dos dados

- **Origem:** [https://github.com/nature4climate/naturebase-data](https://github.com/nature4climate/naturebase-data)
- **Tipo de dado:** Áreas prioritárias para soluções baseadas na natureza (NbS)
- **Formato original:** `.zip` contendo `.shp`
- **Tipo de coleta:** Scraping do repositório GitHub

---

## 📊 Diagrama de Fluxo ETL

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
