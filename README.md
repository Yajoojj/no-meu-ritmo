# No Meu Ritmo!

Aplicacao completa de organizacao de estudos feita para atividade universitaria. O projeto contem backend em Flask, frontend em Flet e uma landing page estatica em HTML com Tailwind CSS.

## Requisitos da atividade

- Backend Flask organizado com Blueprints.
- Pelo menos 2 endpoints GET documentados com Swagger/Docstring.
- Pelo menos 1 endpoint POST com validacao usando Pydantic.
- Frontend Flet que lista dados vindos de endpoint GET.
- Formulario Flet que consome endpoint POST e exibe feedback.
- Landing page com nome, descricao e instrucoes de execucao.
- Dados em memoria por padrao, com persistencia opcional no Supabase/Postgres.

## O que o sistema faz

- Lista materias cadastradas.
- Mostra um plano de estudos para o dia.
- Registra sessoes de estudo com materia, tipo, duracao, foco e observacao.
- Gera relatorio em PDF para download.
- Valida o cadastro com Pydantic.
- Documenta a API com Swagger.
- Nao usa dados mockados na interface: materias e plano sao calculados a partir das sessoes reais registradas.

## Tecnologias

- Python
- Flask
- Flask Blueprints
- Pydantic
- Flasgger / Swagger
- Flet
- HTML
- Tailwind CSS
- Supabase/Postgres opcional

## Como rodar localmente

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependencias:

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
- Materias: <http://127.0.0.1:5000/api/materias>
- Plano do dia: <http://127.0.0.1:5000/api/plano-hoje>
- Sessoes: <http://127.0.0.1:5000/api/sessoes>
- Relatorio PDF: <http://127.0.0.1:5000/api/relatorio.pdf>

Em outro terminal, rode o frontend:

```bash
python frontend/main.py
```

## Supabase opcional

O projeto funciona sem banco, usando memoria/localStorage, como permitido na atividade. Para persistir materias e sessoes no Supabase/Postgres:

1. Rode o SQL de `docs/supabase.sql` no SQL Editor do Supabase.
2. Configure as variaveis:

```bash
SUPABASE_URL=https://cjdtjvwrikpgzprjhmty.supabase.co
SUPABASE_KEY=sua_chave_publishable
```

Na Vercel, cadastre as mesmas variaveis em Production, Preview e Development.

Com essas tabelas criadas, o backend usa a Supabase para:

- `GET /api/materias`
- `POST /api/materias`
- `PUT /api/materias/<id>`
- `DELETE /api/materias/<id>`
- `GET /api/sessoes`
- `POST /api/sessoes`

## Exemplo de POST

Endpoint:

```text
POST /api/sessoes
```

Corpo:

```json
{
  "materia": "Programacao Web",
  "tipo_estudo": "projeto",
  "duracao_minutos": 45,
  "nivel_foco": 4,
  "observacao": "Testei a integracao do Flet com a API."
}
```

## Testes

```bash
python -m unittest
```

## Deploy

A aplicacao esta preparada para deploy na Vercel usando Flask. A landing page fica na rota principal, a API fica em `/api` e a documentacao Swagger fica em `/apidocs/`.

Repositorio publico: <https://github.com/Yajoojj/no-meu-ritmo>
