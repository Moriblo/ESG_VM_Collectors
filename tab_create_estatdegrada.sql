-- 🗃️ Cria a tabela de estatísticas de degradação ambiental
CREATE TABLE estatdegrada (
    id SERIAL PRIMARY KEY,
    
    estado VARCHAR(2),                  -- Sigla do estado (UF)
    bioma VARCHAR(50),                  -- Nome do bioma
    municipio VARCHAR(100),             -- Nome do município
    id_municipio_ibge VARCHAR(10),      -- Código IBGE do município
    categoria_degradacao VARCHAR(100),  -- Tipo de degradação
    area_ha NUMERIC(12,2),              -- Área degradada em hectares
    ano INTEGER,                        -- Ano da observação

    fonte VARCHAR(50),                  -- Nome da fonte dos dados
    arquivo_origem VARCHAR(200),        -- Nome do arquivo .xlsx
    planilha_origem VARCHAR(100),       -- Aba da planilha original

    criado_em TIMESTAMP DEFAULT NOW()   -- Timestamp de inserção
);
