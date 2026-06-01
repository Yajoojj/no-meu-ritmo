-- Dados iniciais equivalentes ao arquivo backend/data.py.

BEGIN;

INSERT INTO materias (id, nome, cor, prioridade, descricao) VALUES
    (1, 'Engenharia de Software', '#2563eb', 'alta', 'Revisar requisitos, casos de uso e organização de projetos.'),
    (2, 'Banco de Dados', '#16a34a', 'media', 'Praticar consultas SQL e modelagem relacional.'),
    (3, 'Programação Web', '#dc2626', 'alta', 'Separar um tempo para APIs, frontend e integração.'),
    (4, 'Estrutura de Dados', '#9333ea', 'baixa', 'Fazer exercícios curtos para manter o conteúdo fresco.')
ON CONFLICT (id) DO UPDATE SET
    nome = EXCLUDED.nome,
    cor = EXCLUDED.cor,
    prioridade = EXCLUDED.prioridade,
    descricao = EXCLUDED.descricao;

INSERT INTO planos_estudo (id, horario, materia_id, tipo, duracao_minutos, meta) VALUES
    (1, '19:00', 3, 'projeto', 50, 'Avançar a atividade prática e testar os endpoints.'),
    (2, '20:00', 2, 'exercicios', 35, 'Resolver algumas consultas com JOIN e GROUP BY.'),
    (3, '20:45', 1, 'revisao', 25, 'Revisar anotações da última aula e marcar dúvidas.')
ON CONFLICT (id) DO UPDATE SET
    horario = EXCLUDED.horario,
    materia_id = EXCLUDED.materia_id,
    tipo = EXCLUDED.tipo,
    duracao_minutos = EXCLUDED.duracao_minutos,
    meta = EXCLUDED.meta;

INSERT INTO sessoes_estudo (id, materia_id, tipo_estudo, duracao_minutos, nivel_foco, observacao) VALUES
    (1, 3, 'projeto', 45, 4, 'Configurei a estrutura inicial do trabalho.')
ON CONFLICT (id) DO UPDATE SET
    materia_id = EXCLUDED.materia_id,
    tipo_estudo = EXCLUDED.tipo_estudo,
    duracao_minutos = EXCLUDED.duracao_minutos,
    nivel_foco = EXCLUDED.nivel_foco,
    observacao = EXCLUDED.observacao;

SELECT setval(pg_get_serial_sequence('materias', 'id'), COALESCE((SELECT MAX(id) FROM materias), 1));
SELECT setval(pg_get_serial_sequence('planos_estudo', 'id'), COALESCE((SELECT MAX(id) FROM planos_estudo), 1));
SELECT setval(pg_get_serial_sequence('sessoes_estudo', 'id'), COALESCE((SELECT MAX(id) FROM sessoes_estudo), 1));

COMMIT;
