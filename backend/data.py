MATERIAS = []
SESSOES = []


def proximo_id_materia() -> int:
    return max((materia["id"] for materia in MATERIAS), default=0) + 1


def proximo_id_sessao() -> int:
    return max((sessao["id"] for sessao in SESSOES), default=0) + 1
