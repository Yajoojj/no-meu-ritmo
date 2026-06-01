LANDING_HTML = """<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>No Meu Ritmo!</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-zinc-50 text-zinc-950 antialiased">
    <main class="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-6 sm:px-8">
      <nav class="flex items-center justify-between border-b border-zinc-200 pb-5">
        <a class="text-base font-semibold tracking-tight" href="/">No Meu Ritmo!</a>
        <div class="flex items-center gap-2">
          <a class="rounded-md border border-zinc-300 px-3 py-2 text-sm font-medium text-zinc-700 transition hover:bg-white" href="/apidocs/">Swagger</a>
          <a class="rounded-md bg-zinc-950 px-3 py-2 text-sm font-medium text-white transition hover:bg-zinc-800" href="/api/materias">API</a>
        </div>
      </nav>
      <section class="grid flex-1 items-center gap-10 py-12 md:grid-cols-[1.05fr_0.95fr] md:py-16">
        <div>
          <p class="text-sm font-medium uppercase tracking-[0.18em] text-zinc-500">Organizador de estudos</p>
          <h1 class="mt-5 max-w-3xl text-5xl font-semibold leading-[1.02] tracking-tight text-zinc-950 md:text-7xl">No Meu Ritmo!</h1>
          <p class="mt-6 max-w-2xl text-lg leading-8 text-zinc-600">
            Aplicacao completa para planejar materias, consultar o plano do dia e registrar sessoes de estudo com foco,
            tempo e observacoes. O backend usa Flask com Blueprints, Swagger e validacao Pydantic; o frontend usa Flet.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <a class="rounded-md bg-zinc-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-zinc-800" href="/apidocs/">Abrir documentacao</a>
            <a class="rounded-md border border-zinc-300 px-5 py-3 text-sm font-semibold text-zinc-800 transition hover:bg-white" href="/api/plano-hoje">Ver plano do dia</a>
          </div>
        </div>
        <div class="border border-zinc-200 bg-white p-5 shadow-sm">
          <div class="flex items-center justify-between border-b border-zinc-100 pb-4">
            <h2 class="text-lg font-semibold">Requisitos atendidos</h2>
            <span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">Pronto</span>
          </div>
          <div class="divide-y divide-zinc-100">
            <div class="py-4"><p class="font-medium">Backend Flask</p><p class="mt-1 text-sm leading-6 text-zinc-600">Blueprints, dois endpoints GET documentados e um POST validado com Pydantic.</p></div>
            <div class="py-4"><p class="font-medium">Frontend Flet</p><p class="mt-1 text-sm leading-6 text-zinc-600">Tela que consome GET e formulario que envia dados para o POST com feedback.</p></div>
            <div class="py-4"><p class="font-medium">Landing Page</p><p class="mt-1 text-sm leading-6 text-zinc-600">Pagina estatica em HTML com Tailwind, descricao do projeto e instrucoes de execucao.</p></div>
          </div>
        </div>
      </section>
      <section class="grid gap-6 border-t border-zinc-200 py-8 md:grid-cols-3">
        <div><h2 class="text-base font-semibold">Backend</h2><p class="mt-2 text-sm leading-6 text-zinc-600">Execute <code class="bg-zinc-200 px-1">python app.py</code> e acesse a API em <code class="bg-zinc-200 px-1">/api</code>.</p></div>
        <div><h2 class="text-base font-semibold">Frontend</h2><p class="mt-2 text-sm leading-6 text-zinc-600">Em outro terminal, rode <code class="bg-zinc-200 px-1">python frontend/main.py</code>.</p></div>
        <div><h2 class="text-base font-semibold">Dados</h2><p class="mt-2 text-sm leading-6 text-zinc-600">Funciona em memoria e tambem pode persistir sessoes no Supabase quando configurado.</p></div>
      </section>
    </main>
  </body>
</html>"""
