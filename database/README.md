# Banco de dados PostgreSQL

Este diretório contém os scripts SQL para transformar os dados em memória da aplicação **No Meu Ritmo!** em um banco PostgreSQL.

A aplicação atualmente possui:

- `materias`: matérias cadastradas.
- `planos_estudo`: blocos do plano de estudos do dia.
- `sessoes_estudo`: sessões de estudo registradas pelo usuário.

## 1. Criar o banco

No terminal, acesse o PostgreSQL:

```bash
psql -U postgres
```

Crie o banco:

```sql
CREATE DATABASE no_meu_ritmo;
```

Saia do `psql`:

```sql
\q
```

## 2. Criar as tabelas

Na raiz do projeto, rode:

```bash
psql -U postgres -d no_meu_ritmo -f database/schema.sql
```

## 3. Inserir dados iniciais

```bash
psql -U postgres -d no_meu_ritmo -f database/seed.sql
```

## 4. Testar consultas

```bash
psql -U postgres -d no_meu_ritmo -f database/queries.sql
```

## 5. String de conexão sugerida

Para integrar com Flask depois:

```env
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/no_meu_ritmo
```

## Estrutura criada

### materias

Guarda as matérias de estudo.

Campos principais:

- `id`
- `nome`
- `cor`
- `prioridade`
- `descricao`

### planos_estudo

Guarda o plano de estudos por data e horário.

Campos principais:

- `id`
- `materia_id`
- `data_plano`
- `horario`
- `tipo`
- `duracao_minutos`
- `meta`
- `status`

### sessoes_estudo

Guarda o histórico real das sessões registradas.

Campos principais:

- `id`
- `materia_id`
- `tipo_estudo`
- `duracao_minutos`
- `nivel_foco`
- `observacao`
- `data_registro`

## Observação

O banco foi modelado para manter compatibilidade com os endpoints atuais:

- `GET /api/materias`
- `GET /api/plano-hoje`
- `GET /api/sessoes`
- `POST /api/sessoes`

O próximo passo é alterar o backend Flask para consultar o PostgreSQL em vez de usar as listas do arquivo `backend/data.py`.
