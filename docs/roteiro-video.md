# Roteiro do video - No Meu Ritmo!

Tempo sugerido: ate 3 minutos.

## 1. Landing page

Abrir `http://127.0.0.1:5000/` e falar:

"Esse e o No Meu Ritmo!, uma aplicacao para organizar estudos, cadastrar materias, registrar sessoes e acompanhar o progresso. A pagina inicial apresenta o projeto, permite acessar o Swagger, abrir a API e usar o painel feito com HTML e Tailwind."

## 2. Aplicacao em Flet

Abrir o Flet com `python frontend/main.py` e falar:

"Aqui esta a interface em Flet. Ela consome os endpoints GET do backend Flask para listar as materias e o plano de estudos do dia."

## 3. Formulario

Preencher o formulario do Flet e falar:

"Agora vou registrar uma sessao de estudo. Eu informo a materia, o tipo de estudo, a duracao, o nivel de foco e uma observacao. Ao salvar, o Flet envia esses dados para o endpoint POST `/api/sessoes`."

Depois de salvar:

"A mensagem de sucesso aparece na tela, indicando que a API recebeu os dados e que a validacao com Pydantic passou corretamente."

## 4. Swagger

Abrir `http://127.0.0.1:5000/apidocs/` e falar:

"Aqui esta o Swagger da API. O projeto usa Flask com Blueprints, e os endpoints estao documentados por docstrings. Vou mostrar os GETs `/api/materias`, `/api/sessoes` e `/api/plano-hoje`, alem do POST `/api/sessoes`."

## 5. Endpoints funcionando

Testar pelo Swagger ou pelo navegador:

"Primeiro executo o GET de materias para ver a lista cadastrada. Depois executo o GET do plano de hoje, que monta uma sugestao com base nos dados registrados. Por fim, testo o POST enviando uma sessao em JSON e a API retorna a sessao criada com status de sucesso."

Fechamento:

"Esse foi o No Meu Ritmo!, uma aplicacao completa com backend Flask, frontend Flet e landing page em HTML com Tailwind. O codigo esta no repositorio do GitHub e a gravacao mostra a aplicacao funcionando ao vivo."
