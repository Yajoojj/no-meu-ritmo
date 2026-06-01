import os

import flet as ft
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/api")
API_AUTH = (
    os.getenv("API_USERNAME", "aluno"),
    os.getenv("API_PASSWORD", "1234"),
)
TOKEN = None


def login_api() -> str:
    global TOKEN
    if TOKEN:
        return TOKEN

    resposta = requests.post(
        f"{API_BASE_URL}/login",
        json={"username": API_AUTH[0], "password": API_AUTH[1]},
        timeout=8,
    )
    resposta.raise_for_status()
    TOKEN = resposta.json()["token"]
    return TOKEN


def api_headers() -> dict:
    return {"Authorization": f"Bearer {login_api()}"}


def borda_card():
    lado = ft.BorderSide(1, "#e2e8f0")
    return ft.Border(lado, lado, lado, lado)


def buscar_json(caminho: str):
    resposta = requests.get(f"{API_BASE_URL}{caminho}", headers=api_headers(), timeout=8)
    resposta.raise_for_status()
    return resposta.json()


def main(page: ft.Page):
    page.title = "No Meu Ritmo!"
    page.window_width = 1100
    page.window_height = 760
    page.padding = 24
    page.bgcolor = "#f8fafc"
    page.theme_mode = ft.ThemeMode.LIGHT

    materias_coluna = ft.Column(spacing=10)
    plano_coluna = ft.Column(spacing=10)
    feedback = ft.Text("", size=14, color="#166534")

    materia = ft.TextField(label="Matéria", hint_text="Ex: Programação Web", expand=True)
    tipo_estudo = ft.Dropdown(
        label="Tipo de estudo",
        options=[
            ft.dropdown.Option("leitura", "Leitura"),
            ft.dropdown.Option("revisao", "Revisão"),
            ft.dropdown.Option("exercicios", "Exercícios"),
            ft.dropdown.Option("projeto", "Projeto"),
        ],
        value="projeto",
        expand=True,
    )
    duracao = ft.TextField(label="Duração em minutos", value="40", keyboard_type=ft.KeyboardType.NUMBER)
    foco = ft.Dropdown(
        label="Nível de foco",
        options=[ft.dropdown.Option(str(numero), str(numero)) for numero in range(1, 6)],
        value="4",
    )
    observacao = ft.TextField(
        label="Observação",
        hint_text="O que você pretende avançar?",
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    def card_materia(item):
        return ft.Container(
            padding=14,
            border_radius=8,
            bgcolor="#ffffff",
            border=borda_card(),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(width=10, height=10, border_radius=5, bgcolor=item["cor"]),
                            ft.Text(item["nome"], weight=ft.FontWeight.BOLD, size=15),
                            ft.Text(item["prioridade"], size=12, color="#64748b"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Text(item["descricao"], size=13, color="#475569"),
                ],
                spacing=6,
            ),
        )

    def card_plano(item):
        return ft.Container(
            padding=14,
            border_radius=8,
            bgcolor="#ffffff",
            border=borda_card(),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(item["horario"], weight=ft.FontWeight.BOLD, color="#0f172a"),
                            ft.Text(f"{item['duracao_minutos']} min", color="#64748b"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(item["materia"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(item["meta"], size=13, color="#475569"),
                ],
                spacing=6,
            ),
        )

    def carregar_dados():
        materias_coluna.controls.clear()
        plano_coluna.controls.clear()
        try:
            for item in buscar_json("/materias"):
                materias_coluna.controls.append(card_materia(item))
            for item in buscar_json("/plano-hoje"):
                plano_coluna.controls.append(card_plano(item))
            feedback.value = "Dados carregados da API."
            feedback.color = "#166534"
        except requests.RequestException:
            feedback.value = "Não consegui conectar na API. Confira se o Flask está rodando na porta 5000."
            feedback.color = "#b91c1c"
        page.update()

    def registrar_sessao(_):
        try:
            payload = {
                "materia": materia.value,
                "tipo_estudo": tipo_estudo.value,
                "duracao_minutos": int(duracao.value),
                "nivel_foco": int(foco.value),
                "observacao": observacao.value,
            }
        except ValueError:
            feedback.value = "Duração e foco precisam ser números."
            feedback.color = "#b91c1c"
            page.update()
            return

        try:
            resposta = requests.post(f"{API_BASE_URL}/sessoes", json=payload, headers=api_headers(), timeout=8)
            dados = resposta.json()
            if resposta.status_code == 201:
                feedback.value = dados["mensagem"]
                feedback.color = "#166534"
                observacao.value = ""
            else:
                feedback.value = dados.get("erro", "Não foi possível registrar a sessão.")
                feedback.color = "#b91c1c"
        except requests.RequestException:
            feedback.value = "A API não respondeu. Veja se o backend está ligado."
            feedback.color = "#b91c1c"
        page.update()

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("No Meu Ritmo!", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Um painel simples para planejar o estudo do dia e registrar sessões reais.",
                                    color="#475569",
                                ),
                            ],
                            spacing=4,
                        ),
                        ft.Button("Atualizar dados", on_click=lambda _: carregar_dados()),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                [ft.Text("Matérias", size=20, weight=ft.FontWeight.BOLD), materias_coluna],
                                spacing=12,
                            ),
                        ),
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                [ft.Text("Plano de hoje", size=20, weight=ft.FontWeight.BOLD), plano_coluna],
                                spacing=12,
                            ),
                        ),
                    ],
                    spacing=18,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    padding=18,
                    border_radius=8,
                    bgcolor="#ffffff",
                    border=borda_card(),
                    content=ft.Column(
                        [
                            ft.Text("Registrar sessão", size=20, weight=ft.FontWeight.BOLD),
                            ft.Row([materia, tipo_estudo], spacing=12),
                            ft.Row([duracao, foco], spacing=12),
                            observacao,
                            ft.Row(
                                [
                                    ft.Button("Salvar sessão", on_click=registrar_sessao),
                                    feedback,
                                ],
                                spacing=16,
                            ),
                        ],
                        spacing=12,
                    ),
                ),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        )
    )
    carregar_dados()


if __name__ == "__main__":
    ft.run(main)
