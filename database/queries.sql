-- Consultas úteis para usar no backend Flask.

-- 1. Listar matérias
SELECT
    id,
    nome,
    cor,
    prioridade,
    descricao
FROM materias
ORDER BY
    CASE prioridade
        WHEN 'alta' THEN 1
        WHEN 'media' THEN 2
        WHEN 'baixa' THEN 3
    END,
    nome;

-- 2. Plano de estudos de hoje
SELECT
    pe.id,
    TO_CHAR(pe.horario, 'HH24:MI') AS horario,
    m.nome AS materia,
    pe.tipo,
    pe.duracao_minutos,
    pe.meta,
    pe.status
FROM planos_estudo pe
JOIN materias m ON m.id = pe.materia_id
WHERE pe.data_plano = CURRENT_DATE
ORDER BY pe.horario;

-- 3. Histórico de sessões
SELECT
    se.id,
    m.nome AS materia,
    se.tipo_estudo,
    se.duracao_minutos,
    se.nivel_foco,
    se.observacao,
    se.data_registro
FROM sessoes_estudo se
JOIN materias m ON m.id = se.materia_id
ORDER BY se.data_registro DESC, se.id DESC;

-- 4. Registrar uma sessão usando o nome da matéria
-- Troque os valores pelos dados recebidos no POST /api/sessoes.
INSERT INTO sessoes_estudo (
    materia_id,
    tipo_estudo,
    duracao_minutos,
    nivel_foco,
    observacao
)
SELECT
    id,
    'projeto',
    45,
    4,
    'Testei a integração do Flet com a API.'
FROM materias
WHERE nome = 'Programação Web'
RETURNING id, materia_id, tipo_estudo, duracao_minutos, nivel_foco, observacao, data_registro;

-- 5. Relatório de tempo estudado por matéria
SELECT
    m.nome AS materia,
    COUNT(se.id) AS total_sessoes,
    COALESCE(SUM(se.duracao_minutos), 0) AS total_minutos,
    ROUND(AVG(se.nivel_foco), 2) AS foco_medio
FROM materias m
LEFT JOIN sessoes_estudo se ON se.materia_id = m.id
GROUP BY m.id, m.nome
ORDER BY total_minutos DESC, m.nome;
