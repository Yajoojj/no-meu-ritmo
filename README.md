# No Meu Ritmo

No Meu Ritmo e uma aplicacao para organizar estudos, registrar sessoes realizadas e acompanhar o progresso por materia. O projeto foi desenvolvido com backend Flask, API documentada com Swagger, validacao Pydantic, interface web em HTML/Tailwind e frontend Flet mantido para atender aos requisitos da atividade.

Aplicacao em producao: <https://no-meu-ritmo.vercel.app>

Repositorio publico: <https://github.com/Yajoojj/no-meu-ritmo>

## Funcionalidades

- Painel web para uso direto no navegador.
- CRUD de materias: criar, listar, editar e excluir.
- Registro de sessoes de estudo com materia, tipo, duracao, foco e observacao.
- Plano de estudo sugerido com base nas materias e no historico.
- Indicadores de tempo planejado, tempo registrado, foco medio e quantidade de sessoes.
- Relatorio em PDF para download.
- API REST documentada no Swagger.
- Persistencia com Supabase/Postgres quando configurado.
- Fallback em memoria/localStorage para manter a aplicacao utilizavel em ambiente local.

## Requisitos da atividade

| Requisito | Implementacao |
| --- | --- |
| Backend Flask | `app.py` e pacote `backend/` |
| Organizacao com Blueprints | `backend/routes/` |
| 2 endpoints GET documentados | `/api/materias`, `/api/plano-hoje`, `/api/sessoes` |
| 1 endpoint POST com Pydantic | `/api/sessoes` e `/api/materias` |
| Frontend Flet consumindo GET e POST | `frontend/main.py` |
| Landing page HTML + Tailwind | `public/index.html` |
| Instrucoes de execucao | Este README |

## Tecnologias

- Python 3
- Flask
- Flask Blueprints
- Pydantic
- Flasgger / Swagger
- Flet
- HTML
- Tailwind CSS
- Supabase/Postgres
- ReportLab para geracao de PDF
- Vercel para deploy

## Estrutura do projeto

```text
.
|-- app.py
|-- backend/
|   |-- __init__.py
|   |-- data.py
|   |-- landing.py
|   |-- schemas.py
|   |-- storage.py
|   `-- routes/
|       |-- materias.py
|       |-- plano.py
|       |-- relatorios.py
|       `-- sessoes.py
|-- frontend/
|   `-- main.py
|-- public/
|   `-- index.html
|-- docs/
|   `-- supabase.sql
|-- tests/
|   `-- test_api.py
|-- requirements.txt
|-- requirements-dev.txt
`-- vercel.json
```

## API

Com o servidor rodando, a documentacao Swagger fica disponivel em:

```text
/apidocs/
```

Endpoints principais:

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/api/materias` | Lista materias |
| GET | `/api/materias/<id>` | Busca uma materia |
| POST | `/api/materias` | Cria materia |
| PUT | `/api/materias/<id>` | Atualiza materia |
| DELETE | `/api/materias/<id>` | Remove materia |
| GET | `/api/plano-hoje` | Lista sugestao de plano |
| GET | `/api/sessoes` | Lista sessoes |
| POST | `/api/sessoes` | Registra sessao |
| GET | `/api/relatorio.pdf` | Baixa relatorio PDF |

Exemplo de cadastro de materia:

```json
{
  "nome": "Programacao Web",
  "prioridade": "alta",
  "cor": "#2563eb",
  "descricao": "APIs, frontend e integracao."
}
```

Exemplo de registro de sessao:

```json
{
  "materia": "Programacao Web",
  "tipo_estudo": "projeto",
  "duracao_minutos": 45,
  "nivel_foco": 4,
  "observacao": "Integrei o frontend com a API."
}
```

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

- Aplicacao web: <http://127.0.0.1:5000/>
- Swagger: <http://127.0.0.1:5000/apidocs/>
- API de materias: <http://127.0.0.1:5000/api/materias>
- API de sessoes: <http://127.0.0.1:5000/api/sessoes>
- Relatorio PDF: <http://127.0.0.1:5000/api/relatorio.pdf>

Para abrir o frontend Flet:

```bash
python frontend/main.py
```

## Configuracao do Supabase

O projeto usa Supabase/Postgres para persistir materias e sessoes quando as variaveis de ambiente estao configuradas.

Crie as tabelas rodando o script:

```text
docs/supabase.sql
```

Variaveis necessarias:

```env
SUPABASE_URL=https://cjdtjvwrikpgzprjhmty.supabase.co
SUPABASE_KEY=sua_chave_publishable
```

Na Vercel, essas variaveis devem estar cadastradas em Production e Development.

## Regras de dados

- Materias possuem nome, prioridade, cor e descricao.
- Sessoes ficam vinculadas a uma materia no banco por `materia_id`.
- O plano do dia e calculado a partir das materias e do tempo registrado.
- O relatorio em PDF usa os dados retornados pela API.

## Testes

Execute:

```bash
python -m unittest -v
```

Os testes cobrem:

- CRUD de materias.
- Listagem sem dados mockados.
- Criacao de sessao.
- Validacao de dados invalidos.
- Geracao de PDF.

## Deploy

O deploy esta configurado para Vercel.

```bash
npx vercel deploy --prod
```

Arquivos relevantes:

- `vercel.json`: configuracao da funcao Python.
- `.python-version`: versao usada no build da Vercel.
- `requirements.txt`: dependencias de producao.

## Observacoes

O projeto nao depende de dados mockados para a interface principal. Quando a Supabase esta configurada, a API usa o banco como fonte de dados. Em ambiente local sem banco, a aplicacao ainda funciona com fallback em memoria/localStorage para facilitar testes e apresentacao.
