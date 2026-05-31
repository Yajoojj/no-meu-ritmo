import unittest

from backend import create_app


class ApiNoMeuRitmoTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_lista_materias(self):
        resposta = self.client.get("/api/materias")
        self.assertEqual(resposta.status_code, 200)
        self.assertGreaterEqual(len(resposta.get_json()), 2)

    def test_lista_plano_hoje(self):
        resposta = self.client.get("/api/plano-hoje")
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("materia", resposta.get_json()[0])

    def test_registra_sessao_valida(self):
        resposta = self.client.post(
            "/api/sessoes",
            json={
                "materia": "Programação Web",
                "tipo_estudo": "projeto",
                "duracao_minutos": 50,
                "nivel_foco": 5,
                "observacao": "Teste automatizado da rota POST.",
            },
        )
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json()["sessao"]["materia"], "Programação Web")

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


if __name__ == "__main__":
    unittest.main()
