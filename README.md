# No Meu Ritmo!

Aplicação pessoal de organização de estudos feita para atividade universitária. O projeto tem backend em Flask, frontend em Flet e uma landing page em HTML com Tailwind CSS.

## O que o sistema faz

- Lista matérias cadastradas.
- Mostra um plano de estudos para o dia.
- Registra sessões de estudo com matéria, tipo, duração, foco e observação.
- Valida o cadastro com Pydantic.
- Documenta a API com Swagger.

Os dados ficam em memória, como permitido na proposta.

## Tecnologias

- Python
- Flask
- Flask Blueprints
- Pydantic
- Flasgger / Swagger
- Flet
- HTML
- Tailwind CSS

## Como rodar

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements-dev.txt
```

Rode o backend:

```bash
python app.py
```

Acesse:

- Landing page: <http://127.0.0.1:5000/>
- Swagger: <http://127.0.0.1:5000/apidocs/>
- Matérias: <http://127.0.0.1:5000/api/materias>
- Plano do dia: <http://127.0.0.1:5000/api/plano-hoje>

Em outro terminal, rode o frontend:

```bash
python frontend/main.py
```

## Exemplo de POST

Endpoint:

```text
POST /api/sessoes
```

Corpo:

```json
{
  "materia": "Programação Web",
  "tipo_estudo": "projeto",
  "duracao_minutos": 45,
  "nivel_foco": 4,
  "observacao": "Testei a integração do Flet com a API."
}
```

## Testes

```bash
python -m unittest
```

## Deploy

A aplicação foi preparada para deploy na Vercel usando o Flask como backend. A landing page fica na rota principal e a API fica em `/api`.

O frontend Flet é executado localmente para a demonstração, porque esse é o uso mais comum da tecnologia pedida na atividade.
