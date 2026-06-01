from datetime import date
from io import BytesIO

from flask import Blueprint, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.storage import listar_materias, listar_sessoes

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.get("/relatorio.pdf")
def baixar_relatorio_pdf():
    """
    Gera um relatorio em PDF com o historico real de estudos.
    ---
    tags:
      - Relatorios
    responses:
      200:
        description: Arquivo PDF com resumo de materias, tempo total e sessoes registradas.
        content:
          application/pdf:
            schema:
              type: string
              format: binary
    """
    buffer = BytesIO()
    sessoes = listar_sessoes()
    materias = listar_materias()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        title="Relatorio No Meu Ritmo",
    )
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("No Meu Ritmo - Relatorio de Estudos", estilos["Title"]),
        Paragraph(f"Gerado em {date.today().isoformat()}", estilos["Normal"]),
        Spacer(1, 18),
    ]

    total_minutos = sum(int(sessao.get("duracao_minutos") or 0) for sessao in sessoes)
    focos = [int(sessao.get("nivel_foco") or 0) for sessao in sessoes if sessao.get("nivel_foco")]
    foco_medio = f"{sum(focos) / len(focos):.1f}" if focos else "-"

    elementos.extend(
        [
            Paragraph("Resumo", estilos["Heading2"]),
            tabela(
                [
                    ["Sessoes registradas", str(len(sessoes))],
                    ["Materias estudadas", str(len(materias))],
                    ["Tempo total", f"{total_minutos} min"],
                    ["Foco medio", foco_medio],
                ]
            ),
            Spacer(1, 16),
            Paragraph("Materias", estilos["Heading2"]),
        ]
    )

    if materias:
        elementos.append(
            tabela(
                [["Materia", "Prioridade", "Sessoes", "Minutos"]]
                + [
                    [
                        materia["nome"],
                        materia["prioridade"],
                        str(materia["total_sessoes"]),
                        str(materia["total_minutos"]),
                    ]
                    for materia in materias
                ],
                header=True,
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma materia registrada ainda.", estilos["Normal"]))

    elementos.extend([Spacer(1, 16), Paragraph("Historico", estilos["Heading2"])])

    if sessoes:
        elementos.append(
            tabela(
                [["Data", "Materia", "Tipo", "Min", "Foco", "Observacao"]]
                + [
                    [
                        sessao.get("data_registro", ""),
                        sessao.get("materia", ""),
                        sessao.get("tipo_estudo", ""),
                        str(sessao.get("duracao_minutos", "")),
                        str(sessao.get("nivel_foco", "")),
                        sessao.get("observacao") or "",
                    ]
                    for sessao in sessoes
                ],
                header=True,
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma sessao registrada ainda.", estilos["Normal"]))

    documento.build(elementos)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"relatorio-no-meu-ritmo-{date.today().isoformat()}.pdf",
    )


def tabela(dados, header=False):
    table = Table(dados, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d4d4d4")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f5f5")),
    ]
    if header:
        style.append(("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"))
    table.setStyle(TableStyle(style))
    return table
