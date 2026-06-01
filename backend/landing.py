from pathlib import Path


def carregar_landing() -> str:
    public_index = Path(__file__).resolve().parent.parent / "public" / "index.html"
    if public_index.exists():
        return public_index.read_text(encoding="utf-8")

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
