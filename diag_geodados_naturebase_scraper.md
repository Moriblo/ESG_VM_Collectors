# Diagrama ETL — Naturebase.org

> Este documento descreve o fluxo de Extração, Transformação e Carga (ETL) originalmente planejado para o coletor [`etl_geodados_naturebase_scraper.py`](./etl_geodados_naturebase_scraper.py), responsável por importar dados da fonte **Naturebase.org** para a tabela `GeoDados`.

---

## ⚠️ Situação atual

O repositório GitHub anteriormente utilizado para coleta automatizada foi removido ou tornado privado:

- ❌ [https://github.com/nature4climate/naturebase-data](https://github.com/nature4climate/naturebase-data) → **Erro 404**

Dessa forma, o processo de scraping e ETL automatizado está temporariamente suspenso.

---

## ⏸️ Status do coletor

- **Status atual:** ⏸️ on hold
- **Motivo:** Fonte de dados indisponível para coleta automatizada
- **Alternativa:** Aguardar nova publicação oficial ou realizar download manual via [https://www.naturebase.org](https://www.naturebase.org)

---

## 🧪 Script relacionado

- [`etl_geodados_naturebase_scraper.py`](./etl_geodados_naturebase_scraper.py) *(em pausa)*

---

## 🔁 Histórico do fluxo ETL planejado (para referência futura)

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
