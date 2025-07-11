# ESG_VM_Collectors

Scripts para realizar: Extraction, Treatment e Loading (ETL) das fontes de dados para carregar nas tabelas definidas nos Datasets.

---

## 🗂️ Scripts coletores de ETL

| Fonte                  | Tabela Alvo       | Diagrama ETL                                                                  | Script Python                                                                      | Status             |
|------------------------|-------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|--------------------|
| Naturebase.org         | GeoDados          | [diag_geodados_naturebase_scraper](./diag_geodados_naturebase_scraper.md)   | [etl_geodados_naturebase_scraper.py](./etl_geodados_naturebase_scraper.py)       | ⏸️ on hold         |
| SICAR                  | GeoDados          | [diag_geodados_sicar](./diag_geodados_sicar.md)                             | [etl_geodados_sicar.py](./etl_geodados_sicar.py)                                 | ⏸️ on hold         |
| Embrapa AgroAPI        | ProjetoNbS        | [diag_projetonbs_embrapa](./diag_projetonbs_embrapa.md)                     | [etl_projetonbs_embrapa.py](./etl_projetonbs_embrapa.py)                         | 🚫 não iniciado    |
| B3 Sustentabilidade    | ProjetoNbS        | [diag_projetonbs_b3sustentabilidade](./diag_projetonbs_b3sustentabilidade.md)| [etl_projetonbs_b3sustentabilidade.py](./etl_projetonbs_b3sustentabilidade.py)   | 🚫 não iniciado    |
| ISE B3                 | FundoESG          | [diag_fundoesg_iseb3](./diag_fundoesg_iseb3.md)                             | [etl_fundoesg_iseb3.py](./etl_fundoesg_iseb3.py)                                 | 🚫 não iniciado    |
| Ações Verdes           | FundoESG          | [diag_fundoesg_acoesverdes](./diag_fundoesg_acoesverdes.md)                 | [etl_fundoesg_acoesverdes.py](./etl_fundoesg_acoesverdes.py)                     | 🚫 não iniciado    |
| Aliança Brasil NbS     | ProjetoNbS        | [diag_projetonbs_alianca](./diag_projetonbs_alianca.md)                     | [etl_projetonbs_alianca.py](./etl_projetonbs_alianca.py)                         | 🚫 não iniciado    |
| MapBiomas              | GeoDados          | [diag_geodados_mapbiomas_scraper](./diag_geodados_mapbiomas_scraper.md)     | [etl_geodados_mapbiomas_scraper.py](./etl_geodados_mapbiomas_scraper.py)         | ⚠️ em testes       |
| GFW                    | GeoDados          | [diag_geodados_gfw_scraper](./diag_geodados_gfw_scraper.md)                 | [etl_geodados_gfw_scraper.py](./etl_geodados_gfw_scraper.py)                     | 🚧 em desenvolvimento |
| OSM                    | GeoDados          | [diag_geodados_osm](./diag_geodados_osm.md)                                 | [etl_geodados_osm.py](./etl_geodados_osm.py)                                     | ⚠️ em testes       |
| MapBiomas Degradação   | EstatDegrada      | [diag_estatdegrada_mapbiomas_degradacao](./diag_estatdegrada_mapbiomas_degradacao.md) | [etl_estatdegrada_mapbiomas_degradacao.py](./etl_estatdegrada_mapbiomas_degradacao.py) | 🚧 em desenvolvimento |

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
| `scraper`        | Informa se o script contém scraping antes do ETL                            |
| `.py`            | Extensão do script Python                                                   |
