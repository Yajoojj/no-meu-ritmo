SESSOES = []


def proximo_id_sessao() -> int:
    return max((sessao["id"] for sessao in SESSOES), default=0) + 1
