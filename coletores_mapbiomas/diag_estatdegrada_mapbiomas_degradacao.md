# Diagrama ETL — MapBiomas Degradação (Estatísticas)

> Este documento descreve o fluxo de Extração, Transformação e Carga (ETL) do coletor [`etl_estatdegrada_mapbiomas_degradacao.py`](./etl_estatdegrada_mapbiomas_degradacao.py), responsável por importar estatísticas do módulo de degradação vegetal publicado pelo MapBiomas para a tabela `EstatDegrada`.

---

## 🎯 Objetivo

Importar dados tabulares de degradação da vegetação nativa por vetor (pastagem, mineração, corte raso, fogo etc.), agregados por bioma, estado e município, e armazená-los em estrutura compatível com estatísticas dimensionais.

---

## 📦 Fonte dos dados

- **Origem:** [https://brasil.mapbiomas.org/dados-do-modulo-mapbiomas-degradacao](https://brasil.mapbiomas.org/dados-do-modulo-mapbiomas-degradacao)
- **Arquivo:** `brazil-degradation-statistics.zip`
- **Formato:** `.xlsx` (múltiplas planilhas)
- **Tipo de dado:** estatísticas tabulares (não geoespaciais)

---

## 📊 Diagrama de Fluxo ETL

```text
[Download do arquivo ZIP]
        ↓
[Extração dos arquivos .xlsx]
        ↓
[Leitura das planilhas com Pandas]
        ↓
[Normalização dos dados (long format, limpeza)]
        ↓
[Inclusão do campo 'fonte' e atributos temporais]
        ↓
[Inserção em tabela GeoDados_Degrada]
