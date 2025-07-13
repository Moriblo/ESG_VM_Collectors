-- 🎯 Inserção de registros de teste
INSERT INTO estatdegrada (
    estado, bioma, municipio, id_municipio_ibge,
    categoria_degradacao, area_ha, ano,
    fonte, arquivo_origem, planilha_origem
) VALUES (
    'AM', 'Amazônia', 'Manaus', '1302603',
    'Desmatamento leve', 1123.45, 2022,
    'mapbiomas_degradacao', 'teste.xlsx', 'Sheet1'
);
