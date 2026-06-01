from pathlib import Path

AUTH_SCRIPT = """
<script>
  (() => {
    const AUTH_KEY = "no-meu-ritmo-auth";
    const originalFetch = window.fetch.bind(window);

    function savedAuth() {
      return sessionStorage.getItem(AUTH_KEY) || "";
    }

    function authHeaders() {
      const token = savedAuth();
      return token ? { Authorization: `Basic ${token}` } : {};
    }

    async function pedirLogin() {
      const usuario = window.prompt("Usuario para ver as materias:", "aluno");
      if (usuario === null) return false;

      const senha = window.prompt("Senha:", "1234");
      if (senha === null) return false;

      sessionStorage.setItem(AUTH_KEY, btoa(`${usuario}:${senha}`));
      return true;
    }

    window.fetch = async (resource, options = {}) => {
      const url = typeof resource === "string" ? resource : resource.url;
      const precisaAuth = url && url.includes("/api/materias");
      const headers = new Headers(options.headers || {});

      if (precisaAuth) {
        Object.entries(authHeaders()).forEach(([key, value]) => headers.set(key, value));
      }

      let response = await originalFetch(resource, { ...options, headers });

      if (precisaAuth && response.status === 401) {
        sessionStorage.removeItem(AUTH_KEY);
        const autenticou = await pedirLogin();
        if (!autenticou) return response;

        const retryHeaders = new Headers(options.headers || {});
        Object.entries(authHeaders()).forEach(([key, value]) => retryHeaders.set(key, value));
        response = await originalFetch(resource, { ...options, headers: retryHeaders });
      }

      return response;
    };
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
