from pathlib import Path

AUTH_SCRIPT = """
<script>
  (() => {
    const AUTH_KEY = "no-meu-ritmo-auth";
    const originalFetch = window.fetch.bind(window);

    function getToken() {
      return sessionStorage.getItem(AUTH_KEY) || "";
    }

    function saveToken(usuario, senha) {
      sessionStorage.setItem(AUTH_KEY, btoa(`${usuario}:${senha}`));
    }

    function clearToken() {
      sessionStorage.removeItem(AUTH_KEY);
    }

    function showOverlay() {
      if (document.getElementById("loginOverlay")) return;

      const overlay = document.createElement("section");
      overlay.id = "loginOverlay";
      overlay.className = "fixed inset-0 z-50 flex items-center justify-center bg-neutral-950/80 px-4";
      overlay.innerHTML = `
        <div class="w-full max-w-md border border-neutral-300 bg-white p-6 shadow-xl">
          <p class="text-xs font-semibold uppercase tracking-[0.22em] text-neutral-500">Acesso</p>
          <h2 class="mt-1 text-2xl font-semibold">No Meu Ritmo!</h2>
          <p class="mt-2 text-sm text-neutral-600">Entre ou crie um cadastro rápido para acessar suas matérias.</p>

          <form id="loginForm" class="mt-5 space-y-3">
            <label class="block">
              <span class="text-sm font-medium">Usuário</span>
              <input id="loginUser" class="mt-1 w-full rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-950" value="aluno" minlength="3" required />
            </label>
            <label class="block">
              <span class="text-sm font-medium">Senha</span>
              <input id="loginPass" type="password" class="mt-1 w-full rounded-md border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-950" value="1234" minlength="4" required />
            </label>
            <p id="loginMsg" class="min-h-5 text-sm font-medium"></p>
            <button class="w-full rounded-md bg-neutral-950 px-4 py-3 text-sm font-semibold text-white hover:bg-neutral-800" type="submit">Entrar</button>
            <button id="signupButton" class="w-full rounded-md border border-neutral-300 bg-white px-4 py-3 text-sm font-semibold hover:bg-neutral-50" type="button">Criar cadastro rápido</button>
          </form>
        </div>
      `;
      document.body.appendChild(overlay);

      const userInput = document.getElementById("loginUser");
      const passInput = document.getElementById("loginPass");
      const msg = document.getElementById("loginMsg");

      async function enviar(url, texto) {
        const usuario = userInput.value.trim();
        const senha = passInput.value;
        msg.className = "min-h-5 text-sm font-medium text-neutral-600";
        msg.textContent = texto;

        const response = await originalFetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: usuario, password: senha })
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
          msg.className = "min-h-5 text-sm font-medium text-red-700";
          msg.textContent = data.erro || "Não foi possível continuar.";
          return;
        }

        saveToken(usuario, senha);
        overlay.remove();
        if (window.loadData) window.loadData();
      }

      document.getElementById("loginForm").addEventListener("submit", (event) => {
        event.preventDefault();
        enviar("/api/login", "Entrando...");
      });

      document.getElementById("signupButton").addEventListener("click", () => {
        enviar("/api/cadastro-rapido", "Criando cadastro...");
      });
    }

    window.fetch = async (resource, options = {}) => {
      const url = typeof resource === "string" ? resource : resource.url;
      const needsLogin = url && url.includes("/api/materias");
      const headers = new Headers(options.headers || {});

      if (needsLogin && getToken()) {
        headers.set("Authorization", `Basic ${getToken()}`);
      }

      const response = await originalFetch(resource, { ...options, headers });

      if (needsLogin && response.status === 401) {
        clearToken();
        showOverlay();
      }

      return response;
    };

    document.addEventListener("DOMContentLoaded", () => {
      const nav = document.querySelector("header nav");
      if (nav && !document.getElementById("logoutButton")) {
        const button = document.createElement("button");
        button.id = "logoutButton";
        button.type = "button";
        button.className = "rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm font-medium hover:bg-neutral-50";
        button.textContent = "Sair";
        button.addEventListener("click", () => {
          clearToken();
          showOverlay();
        });
        nav.appendChild(button);
      }

      if (!getToken()) {
        showOverlay();
      }
    });
  })();
</script>
"""


def carregar_landing() -> str:
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir.parent / "public" / "index.html",
        base_dir / "static_index.html",
    ]
    for index_html in candidates:
        if index_html.exists():
            html = index_html.read_text(encoding="utf-8")
            if "no-meu-ritmo-auth" not in html:
                html = html.replace("<script>", f"{AUTH_SCRIPT}\n    <script>", 1)
            return html

    return (
        "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>No Meu Ritmo</title></head><body>"
        "<main style='font-family:Arial,sans-serif;max-width:720px;margin:64px auto;padding:24px'>"
        "<h1>No Meu Ritmo</h1>"
        "<p>O arquivo public/index.html nao foi encontrado neste ambiente.</p>"
        "<p>A API continua disponivel em /api/materias e a documentacao em /apidocs/.</p>"
        "</main></body></html>"
    )
