from datetime import date

MATERIAS = [
    {
        "id": 1,
        "nome": "Engenharia de Software",
        "cor": "#2563eb",
        "prioridade": "alta",
        "descricao": "Revisar requisitos, casos de uso e organização de projetos.",
    },
    {
        "id": 2,
        "nome": "Banco de Dados",
        "cor": "#16a34a",
        "prioridade": "media",
        "descricao": "Praticar consultas SQL e modelagem relacional.",
    },
    {
        "id": 3,
        "nome": "Programação Web",
        "cor": "#dc2626",
        "prioridade": "alta",
        "descricao": "Separar um tempo para APIs, frontend e integração.",
    },
    {
        "id": 4,
        "nome": "Estrutura de Dados",
        "cor": "#9333ea",
        "prioridade": "baixa",
        "descricao": "Fazer exercícios curtos para manter o conteúdo fresco.",
    },
]

PLANO_HOJE = [
    {
        "id": 1,
        "horario": "19:00",
        "materia": "Programação Web",
        "tipo": "projeto",
        "duracao_minutos": 50,
        "meta": "Avançar a atividade prática e testar os endpoints.",
    },
    {
        "id": 2,
        "horario": "20:00",
        "materia": "Banco de Dados",
        "tipo": "exercicios",
        "duracao_minutos": 35,
        "meta": "Resolver algumas consultas com JOIN e GROUP BY.",
    },
    {
        "id": 3,
        "horario": "20:45",
        "materia": "Engenharia de Software",
        "tipo": "revisao",
        "duracao_minutos": 25,
        "meta": "Revisar anotações da última aula e marcar dúvidas.",
    },
]

SESSOES = [
    {
        "id": 1,
        "materia": "Programação Web",
        "tipo_estudo": "projeto",
        "duracao_minutos": 45,
        "nivel_foco": 4,
        "observacao": "Configurei a estrutura inicial do trabalho.",
        "data_registro": date.today().isoformat(),
    }
]


def proximo_id_sessao() -> int:
    return max((sessao["id"] for sessao in SESSOES), default=0) + 1
