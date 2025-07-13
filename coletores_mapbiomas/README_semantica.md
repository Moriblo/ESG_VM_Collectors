# 🧠 README_semantica.md — Módulo de Enriquecimento Técnico MapBiomas

Este documento descreve o funcionamento do módulo `semantica_mapbiomas.py`, responsável por atribuir significados técnicos aos campos detectados nas planilhas de estatísticas ambientais da plataforma MapBiomas.

---

## 🎯 Objetivo do módulo

- Carregar configurações e cache local de definições
- Buscar definições semânticas de campos técnicos via:
  - Glossário oficial do MapBiomas
  - Cache local manualmente alimentado
- Atualizar e persistir definições no arquivo `referencias_mapbiomas.json`
- Enriquecer perfis de análise durante o processo ETL

---

## 🧩 Campos semânticos detectados e suas definições técnicas

| Campo        | Definição sugerida                                                                 | Fonte técnica                                                 |
|--------------|--------------------------------------------------------------------------------------|---------------------------------------------------------------|
| `feature_id` | Identificador único da feição espacial no conjunto de dados                         | [GeoJSON Specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946) |
| `theme`      | Tema principal da classificação, como degradação, vegetação secundária ou mineração | [MapBiomas Glossário Oficial](https://brasil.mapbiomas.org/glossario) |
| `geocode`    | Código geográfico que representa o estado ou município da feição                    | [IBGE Geocódigos](https://www.ibge.gov.br) |
| `class_id`   | Código da classe de uso/cobertura conforme a legenda oficial MapBiomas              | [Legenda CSV – Coleção 8](https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_8/degradation/statistics/mapbiomas-legend.csv) |
| `color`      | Código hexadecimal que representa a cor associada à classe                          | Padrão cartográfico em GIS (ex: QGIS, ArcGIS) |
| `level_0` a `level_4` | Hierarquias temáticas que detalham a classificação de uso/cobertura       | Estrutura interna das planilhas XLSX da Coleção 8 MapBiomas |
| `raw`        | Valor bruto extraído da planilha original                                           | Conceito estatístico comum: dados não tratados |
| `value`      | Valor numérico estimado para a feição no ano analisado                              | Representação direta das colunas anuais (ex: 1986–2022) |
| `key`        | Identificador auxiliar usado para indexação ou associação                           | Boas práticas de modelagem em ETL e bancos relacionais |

---

## 🧠 Como o módulo funciona

### 🔧 Funções principais

- `carregar_config_global()` → Lê parâmetros do `setup.json`
- `carregar_cache_local()` → Carrega ou inicializa o `referencias_mapbiomas.json`
- `buscar_glossario_online(termo)` → Scraping leve do glossário oficial
- `atualizar_cache_com_legenda()` → Processa o CSV oficial da legenda e atualiza o cache
- `buscar_definicao(campo, cache)` → Busca definição no cache e na web; atualiza se encontrado

---

## 📁 Arquivos utilizados

| Arquivo                    | Finalidade                                                       |
|---------------------------|-------------------------------------------------------------------|
| `setup.json`              | Parâmetros globais usados por todos os módulos                   |
| `referencias_mapbiomas.json` | Cache local com definições conhecidas ou editadas manualmente |
| `mapbiomas-legend.csv`    | Arquivo de legenda oficial (opcional) para perfis que usam `class_id` |

---

## 🔒 Recomendações de uso

- Para perfis que **não** utilizam `class_id`, mantenha `"usar_legenda_csv": false` no `setup.json`
- Alimente manualmente o `referencias_mapbiomas.json` com significados recorrentes
- Verifique a estrutura do glossário online caso deseje ampliar o scraping
- Mantenha o cache sob controle de versão (`git`) para garantir rastreabilidade

---

**Versão da documentação:** 1.0  
**Autor:** MOACYR com suporte técnico de Microsoft Copilot