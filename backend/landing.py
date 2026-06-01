from pathlib import Path

AUTH_MARKER = "no-meu-ritmo-access-overlay"

AUTH_SCRIPT = """
<script id="no-meu-ritmo-access-overlay">
  (() => {
    const AUTH_KEY = "no-meu-ritmo-auth";
    const USER_KEY = "no-meu-ritmo-user";
    const originalFetch = window.fetch.bind(window);

    function getToken() {
      return sessionStorage.getItem(AUTH_KEY) || "";
    }

    function getUser() {
      return sessionStorage.getItem(USER_KEY) || "";
    }

    window.noMeuRitmoCurrentUser = getUser;

    function setAccess(username, token) {
      sessionStorage.setItem(AUTH_KEY, token);
      sessionStorage.setItem(USER_KEY, username);
    }

    function clearAccess() {
      sessionStorage.removeItem(AUTH_KEY);
      sessionStorage.removeItem(USER_KEY);
    }

    function closeOverlay() {
      const overlay = document.getElementById("loginOverlay");
      if (overlay) overlay.remove();
      document.body.classList.remove("overflow-hidden");
    }

    function showOverlay(message = "") {
      if (document.getElementById("loginOverlay")) return;

      document.body.classList.add("overflow-hidden");
      const overlay = document.createElement("section");
      overlay.id = "loginOverlay";
      overlay.className = "fixed inset-0 z-50 flex items-center justify-center bg-neutral-950/80 px-4 backdrop-blur-sm";
      overlay.innerHTML = `
        <div class="w-full max-w-md overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-2xl">
          <div class="bg-neutral-950 px-6 py-5 text-white">
            <p class="text-xs font-semibold uppercase tracking-[0.24em] text-neutral-400">Acesso ao painel</p>
            <h2 class="mt-2 text-2xl font-semibold">No Meu Ritmo!</h2>
            <p class="mt-2 text-sm text-neutral-300">Entre ou crie um cadastro rápido para acessar suas matérias.</p>
          </div>

          <form id="loginForm" class="space-y-4 p-6">
            <label class="block">
              <span class="text-sm font-medium">Usuário</span>
              <input id="loginUser" autocomplete="username" class="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-950" value="aluno" minlength="3" required />
            </label>
            <label class="block">
              <span class="text-sm font-medium">Senha</span>
              <input id="loginPass" autocomplete="current-password" type="password" class="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 outline-none focus:border-neutral-950" value="1234" minlength="4" required />
            </label>

            <p id="loginMsg" class="min-h-5 text-sm font-medium">${message}</p>

            <div class="grid gap-2 sm:grid-cols-2">
              <button id="loginButton" class="rounded-lg bg-neutral-950 px-4 py-3 text-sm font-semibold text-white hover:bg-neutral-800 disabled:cursor-not-allowed disabled:bg-neutral-400" type="submit">Entrar</button>
              <button id="signupButton" class="rounded-lg border border-neutral-300 bg-white px-4 py-3 text-sm font-semibold hover:bg-neutral-50 disabled:cursor-not-allowed disabled:bg-neutral-100" type="button">Cadastrar</button>
            </div>

            <p class="text-xs leading-relaxed text-neutral-500">Cadastro rápido para demonstração acadêmica. Use um usuário com pelo menos 3 caracteres e senha com pelo menos 4.</p>
          </form>
        </div>
      `;
      document.body.appendChild(overlay);

      const userInput = document.getElementById("loginUser");
      const passInput = document.getElementById("loginPass");
      const msg = document.getElementById("loginMsg");
      const loginButton = document.getElementById("loginButton");
      const signupButton = document.getElementById("signupButton");

      async function submitAccess(url, loadingText) {
        const username = userInput.value.trim();
        const password = passInput.value;

        if (username.length < 3 || password.length < 4) {
          msg.className = "min-h-5 text-sm font-medium text-red-700";
          msg.textContent = "Informe usuário e senha válidos.";
          return;
        }

        loginButton.disabled = true;
        signupButton.disabled = true;
        msg.className = "min-h-5 text-sm font-medium text-neutral-600";
        msg.textContent = loadingText;

        try {
          const response = await originalFetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
          });
          const data = await response.json().catch(() => ({}));

          if (!response.ok) {
            throw new Error(data.erro || "Não foi possível continuar.");
          }

          if (!data.token) {
            throw new Error("Login sem token retornado pela API.");
          }

          setAccess(data.usuario?.username || username, data.token);
          closeOverlay();
          await window.loadData?.();
        } catch (error) {
          msg.className = "min-h-5 text-sm font-medium text-red-700";
          msg.textContent = error.message;
        } finally {
          loginButton.disabled = false;
          signupButton.disabled = false;
        }
      }

      document.getElementById("loginForm").addEventListener("submit", (event) => {
        event.preventDefault();
        submitAccess("/api/login", "Entrando...");
      });

      signupButton.addEventListener("click", () => {
        submitAccess("/api/cadastro-rapido", "Criando cadastro...");
      });
    }

    window.fetch = async (resource, options = {}) => {
      const url = typeof resource === "string" ? resource : resource.url;
      const needsLogin = url && url.includes("/api/")
        && !url.includes("/api/login")
        && !url.includes("/api/cadastro-rapido");
      const headers = new Headers(options.headers || {});

      if (needsLogin && getToken()) {
        headers.set("Authorization", "Bearer " + getToken());
      }

      const response = await originalFetch(resource, { ...options, headers });

      if (needsLogin && response.status === 401) {
        clearAccess();
        showOverlay("Faça login para continuar.");
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
          clearAccess();
          showOverlay("Você saiu da conta.");
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
            if AUTH_MARKER not in html:
                html = html.replace("<script>", AUTH_SCRIPT + "\n    <script>", 1)
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
