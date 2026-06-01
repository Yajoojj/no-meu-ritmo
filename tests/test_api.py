import unittest

from backend import create_app
from backend.data import MATERIAS, SESSOES


class ApiNoMeuRitmoTest(unittest.TestCase):
    def setUp(self):
        MATERIAS.clear()
        SESSOES.clear()
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def registrar_sessao(self):
        return self.client.post(
            "/api/sessoes",
            json={
                "materia": "Programacao Web",
                "tipo_estudo": "projeto",
                "duracao_minutos": 50,
                "nivel_foco": 5,
                "observacao": "Teste automatizado da rota POST.",
            },
        )

    def test_lista_materias_sem_mock(self):
        resposta = self.client.get("/api/materias")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [])

    def test_crud_materias(self):
        criada = self.client.post(
            "/api/materias",
            json={
                "nome": "Redes",
                "prioridade": "alta",
                "cor": "#0f766e",
                "descricao": "Revisar protocolos.",
            },
        )
        self.assertEqual(criada.status_code, 201)
        materia = criada.get_json()["materia"]
        self.assertEqual(materia["nome"], "Redes")

        atualizada = self.client.put(
            f"/api/materias/{materia['id']}",
            json={
                "nome": "Redes de Computadores",
                "prioridade": "media",
                "cor": "#2563eb",
                "descricao": "Camadas e protocolos.",
            },
        )
        self.assertEqual(atualizada.status_code, 200)
        self.assertEqual(atualizada.get_json()["materia"]["nome"], "Redes de Computadores")

        removida = self.client.delete(f"/api/materias/{materia['id']}")
        self.assertEqual(removida.status_code, 200)
        self.assertEqual(self.client.get("/api/materias").get_json(), [])

    def test_registro_cria_materia_e_plano(self):
        resposta = self.registrar_sessao()
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json()["sessao"]["materia"], "Programacao Web")

        materias = self.client.get("/api/materias").get_json()
        plano = self.client.get("/api/plano-hoje").get_json()

        self.assertEqual(materias[0]["nome"], "Programacao Web")
        self.assertEqual(plano[0]["materia"], "Programacao Web")

    def test_exclui_materia_criada_por_sessao(self):
        self.registrar_sessao()
        materia = self.client.get("/api/materias").get_json()[0]

        removida = self.client.delete(f"/api/materias/{materia['id']}")

        self.assertEqual(removida.status_code, 200)
        self.assertEqual(removida.get_json()["materia"]["nome"], "Programacao Web")
        self.assertEqual(self.client.get("/api/materias").get_json(), [])

    def test_exclui_materia_criada_por_sessao_usando_nome(self):
        self.registrar_sessao()

        removida = self.client.delete("/api/materias-por-nome/Programacao%20Web")

        self.assertEqual(removida.status_code, 200)
        self.assertEqual(removida.get_json()["materia"]["nome"], "Programacao Web")
        self.assertEqual(self.client.get("/api/materias").get_json(), [])

    def test_rejeita_sessao_invalida(self):
        resposta = self.client.post(
            "/api/sessoes",
            json={
                "materia": "",
                "tipo_estudo": "decorar",
                "duracao_minutos": 0,
                "nivel_foco": 8,
            },
        )
        self.assertEqual(resposta.status_code, 422)

    def test_relatorio_pdf(self):
        self.registrar_sessao()
        resposta = self.client.get("/api/relatorio.pdf")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.content_type, "application/pdf")
        self.assertTrue(resposta.data.startswith(b"%PDF"))

    def test_landing_mantem_formularios_interativos(self):
        resposta = self.client.get("/")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn('document.addEventListener("click", async (event)', html)
        self.assertIn('id="subjectForm" method="post" action="/api/materias"', html)
        self.assertIn('id="sessionForm" method="post" action="/api/sessoes"', html)
        self.assertIn("clearLegacyQueryString();", html)


if __name__ == "__main__":
    unittest.main()
