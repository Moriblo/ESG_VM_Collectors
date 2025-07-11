# Diagrama ETL — SICAR

> Este documento descreve o fluxo de Extração, Transformação e Carga (ETL) planejado para o coletor [`etl_geodados_sicar.py`](./etl_geodados_sicar.py), responsável por importar dados do **Sistema Nacional de Cadastro Ambiental Rural (SICAR)** para a tabela `GeoDados`.

---

## ⚠️ Situação atual

O portal anteriormente vinculado ([https://www.gov.br/sicar](https://www.gov.br/sicar)) está indisponível.

O site oficial ativo é:

🔗 [https://www.car.gov.br](https://www.car.gov.br)

Porém, não há links diretos para shapefiles em lote. O processo de coleta requer interação manual com CAPTCHA e preenchimento de e-mail — o que inviabiliza scraping ou automação direta.

---

## ⏸️ Status do coletor

- **Status atual:** ⏸️ on hold
- **Motivo:** Interface do portal bloqueia download automatizado
- **Alternativa atual:** Download manual por estado ou município

---

## ✅ O que é possível automatizar

- **ETL**: leitura, transformação e carga dos shapefiles baixados manualmente
- **Organização por UF/município**: o script pode processar em lote
- **Validação + inserção em banco de dados**: totalmente automatizável

---

## 📊 Diagrama de Fluxo ETL (semi-automatizado)

```text
[Download manual dos arquivos .zip por estado/município]
        ↓
[Organização em pastas por UF ou município]
        ↓
[Leitura dos shapefiles com GeoPandas]
        ↓
[Conversão de CRS para EPSG:4326 (WGS84)]
        ↓
[Empacotamento dos atributos em JSONB]
        ↓
[Inserção em tabela GeoDados]
        ↓
[Armazenamento do campo geometry como GEOMETRY(Geometry, 4326) via PostGIS]
