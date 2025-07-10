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
