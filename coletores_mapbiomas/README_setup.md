# ⚙️ setup.json — Configurações Globais do Pipeline MapBiomas

Este arquivo centraliza todas as variáveis utilizadas pelo projeto, permitindo ajustes rápidos e consistentes nos scripts `etl_estatdegrada_mapbiomas_degradacao_inspect.py` e `semantica_mapbiomas.py`.

---

## 🎯 Finalidade

- Evitar alterações diretas nos arquivos `.py`
- Facilitar manutenção, reuso e versionamento
- Permitir controle dinâmico de comportamento (como atualizar ou não o JSON de perfis)
- Organizar fontes externas e caminhos internos de maneira declarativa

---

## 🧩 Tabela de Campos

| Campo                          | Descrição                                                                                      | Utilizado em                                     |
|-------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------|
| `atualizar_json`              | Se `true`, o dicionário do perfil ativo será atualizado automaticamente                        | `etl_estatdegrada_mapbiomas_degradacao_inspect.py` |
| `arquivo_perfis`              | Nome do arquivo JSON com os perfis disponíveis e o perfil ativo                                | Ambos os scripts                                 |
| `cache_referencias_path`      | Caminho do arquivo JSON que armazena o cache local de significados técnicos                   | Ambos os scripts                                 |
| `url_legenda_csv`             | URL oficial do MapBiomas para o download do arquivo de legenda (`mapbiomas-legend.csv`)       | `semantica_mapbiomas.py`                         |
| `url_glossario_oficial`       | URL da página de glossário técnico do MapBiomas, usada para scraping leve                     | `semantica_mapbiomas.py`                         |
| `timeout_conexao`             | Tempo limite (em segundos) para conexões externas via `requests`                              | `semantica_mapbiomas.py`                         |
| `limpar_csv_legenda_apos_uso`| Se `true`, o `mapbiomas-legend.csv` será excluído após leitura                                | `semantica_mapbiomas.py`                         |
| `backup_prefix`               | Prefixo dos arquivos de backup do JSON de perfis                                               | `etl_estatdegrada_mapbiomas_degradacao_inspect.py` |
| `backup_timestamp_format`     | Formato de timestamp utilizado nos nomes dos backups                                           | `etl_estatdegrada_mapbiomas_degradacao_inspect.py` |

---

## 🛠️ Exemplo de uso nos scripts

```python
cfg = carregar_config_global()
ARQUIVO_PERFIS = cfg.get("arquivo_perfis", "perfis_xlsx.json")
atualizar_json = cfg.get("atualizar_json", True)
