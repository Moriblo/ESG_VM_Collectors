# Diagrama ETL — SICAR

> Este documento descreve o fluxo de Extração, Transformação e Carga (ETL) planejado para o coletor [`etl_geodados_sicar.py`](./etl_geodados_sicar.py), responsável por importar dados do **Sistema Nacional de Cadastro Ambiental Rural (SICAR)** para a tabela `GeoDados`.

---

## 🎯 Objetivo

Importar dados geoespaciais de imóveis rurais cadastrados no SICAR, com atributos como `estado`, `municipio`, `tipo_imovel`, `area_total`, entre outros, e armazená-los na tabela `GeoDados` com estrutura genérica baseada em `JSONB` e `GEOMETRY`.

---

## 📦 Fonte dos dados

- **Origem:** [https://www.gov.br/sicar](https://www.gov.br/sicar)
- **Tipo de dado:** Cadastro Ambiental Rural (CAR)
- **Formato original:** `.zip` contendo `.shp` por estado
- **Tipo de coleta:** Download manual ou automatizado por estado (a depender da disponibilidade dos links)

---

## 📊 Diagrama de Fluxo ETL

```text
[Download dos arquivos .zip por estado (manual ou automatizado)]
        ↓
[Extração dos arquivos .shp]
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
