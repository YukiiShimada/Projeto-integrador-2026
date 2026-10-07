-- Consultas SQL para o banco banco.db
-- Tabela: atendimentos

-- 1. Conferência: total de atendimentos carregados
SELECT COUNT(*) AS total_atendimentos
FROM atendimentos;

-- 2. Variável 1: atendimentos por período
SELECT
    substr(data_entrada, 1, 7) AS periodo,
    COUNT(*) AS total_atendimentos
FROM atendimentos
WHERE data_entrada IS NOT NULL
GROUP BY periodo
ORDER BY periodo;

-- 3. Variável 2: atendimentos por sexo
SELECT
    COALESCE(NULLIF(sexo, ''), 'Não informado') AS sexo,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY sexo
ORDER BY total_atendimentos DESC;

-- 4. Variável 3: atendimentos por cidade
SELECT
    COALESCE(NULLIF(cidade, ''), 'Não informado') AS cidade,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY cidade
ORDER BY total_atendimentos DESC;

-- 5. Detalhamento por bairro
SELECT
    COALESCE(NULLIF(bairro, ''), 'Não informado') AS bairro,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY bairro
ORDER BY total_atendimentos DESC;

-- 6. Atendimentos por especialidade
SELECT
    COALESCE(NULLIF(especialidade, ''), 'Não informado') AS especialidade,
    COUNT(*) AS total_atendimentos
FROM atendimentos
GROUP BY especialidade
ORDER BY total_atendimentos DESC;