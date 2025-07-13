-- 📊 View agregada por estado e ano
CREATE OR REPLACE VIEW estatdegrada_uf_ano AS
SELECT
    estado,
    ano,
    COUNT(*) AS registros,
    SUM(area_ha) AS area_total_ha
FROM estatdegrada
GROUP BY estado, ano;
