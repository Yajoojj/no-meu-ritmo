# Roteiro do vídeo - No Meu Ritmo!

Tempo sugerido: até 3 minutos.

## 1. Landing page

Abrir a página inicial e falar:

"Esse é o No Meu Ritmo!, um organizador de estudos simples que eu fiz para controlar matérias, plano do dia e sessões de estudo. A landing page apresenta o objetivo do projeto, as tecnologias usadas e como rodar a aplicação."

## 2. Aplicação em Flet

Abrir o app em Flet e falar:

"Aqui no aplicativo eu consigo ver as matérias cadastradas e o plano de estudos sugerido para hoje. Esses dados vêm da API Flask pelos endpoints GET."

## 3. Formulário

Preencher o formulário e falar:

"Agora vou registrar uma sessão de estudo. Eu informo a matéria, o tipo de estudo, a duração, o nível de foco e uma observação. Quando salvo, o Flet envia esses dados para o endpoint POST da API."

Depois de salvar:

"A mensagem de sucesso aparece na tela, mostrando que o cadastro foi recebido e validado."

## 4. Swagger

Abrir `/apidocs/` e falar:

"Aqui está o Swagger da API. Os endpoints foram documentados com docstrings. Temos os GETs de matérias e plano do dia, e o POST de sessões com validação usando Pydantic."

## 5. Endpoints

Testar pelo Swagger:

"Vou executar o GET de matérias, depois o GET do plano de hoje. Por fim, vou testar o POST enviando uma sessão de estudo em JSON. A API retorna a sessão criada com status de sucesso."

Fechamento:

"Esse foi o No Meu Ritmo!, feito com Flask, Flet e Tailwind, usando dados em memória como permitido na atividade."
