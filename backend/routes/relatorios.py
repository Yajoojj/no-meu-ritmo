from datetime import date
from io import BytesIO

from flask import Blueprint, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.auth import usuario_atual_ou_erro
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
    """
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro

    buffer = BytesIO()
    sessoes = listar_sessoes(usuario)
    materias = listar_materias(usuario)

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Relatorio No Meu Ritmo",
    )
    estilos = getSampleStyleSheet()
    estilos.add(
        ParagraphStyle(
            name="Muted",
            parent=estilos["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#525252"),
            leading=12,
        )
    )

    total_minutos = sum(int(sessao.get("duracao_minutos") or 0) for sessao in sessoes)
    focos = [int(sessao.get("nivel_foco") or 0) for sessao in sessoes if sessao.get("nivel_foco")]
    foco_medio = f"{sum(focos) / len(focos):.1f}" if focos else "-"

    elementos = [
        faixa_titulo(estilos),
        Spacer(1, 14),
        cards_resumo(len(sessoes), len(materias), total_minutos, foco_medio),
        Spacer(1, 18),
        Paragraph("Materias", estilos["Heading2"]),
    ]

    if materias:
        elementos.append(
            tabela(
                [["Materia", "Prioridade", "Sessoes", "Minutos"]]
                + [
                    [
                        materia["nome"],
                        materia.get("prioridade", "media"),
                        str(materia.get("total_sessoes", 0)),
                        str(materia.get("total_minutos", 0)),
                    ]
                    for materia in materias
                ],
                header=True,
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma materia cadastrada ainda.", estilos["Muted"]))

    elementos.extend([Spacer(1, 18), Paragraph("Historico", estilos["Heading2"])])

    if sessoes:
        for sessao in sessoes:
            elementos.append(card_sessao(sessao, estilos))
            elementos.append(Spacer(1, 8))
    else:
        elementos.append(Paragraph("Nenhuma sessao registrada ainda.", estilos["Muted"]))

    documento.build(elementos)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"relatorio-no-meu-ritmo-{date.today().isoformat()}.pdf",
    )


def faixa_titulo(estilos):
    return Table(
        [
            [
                Paragraph("<font color='white'><b>No Meu Ritmo</b></font>", estilos["Title"]),
                Paragraph(
                    f"<font color='white'>Relatorio gerado em {date.today().isoformat()}</font>",
                    estilos["Normal"],
                ),
            ]
        ],
        colWidths=[95 * mm, 65 * mm],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#171717")),
                ("BOX", (0, 0), (-1, -1), 0, colors.HexColor("#171717")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        ),
    )


def cards_resumo(total_sessoes, total_materias, total_minutos, foco_medio):
    dados = [
        ["Sessoes", str(total_sessoes)],
        ["Materias", str(total_materias)],
        ["Tempo total", f"{total_minutos} min"],
        ["Foco medio", foco_medio],
    ]
    return Table(
        [[card[0], card[1]] for card in dados],
        colWidths=[35 * mm, 30 * mm],
        style=TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d4d4d4")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#525252")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        ),
    )


def card_sessao(sessao, estilos):
    titulo = sessao.get("materia") or "Materia"
    meta = (
        f"{sessao.get('data_registro', '')} | {sessao.get('tipo_estudo', '')} | "
        f"{sessao.get('duracao_minutos', 0)} min | foco {sessao.get('nivel_foco', '-')}"
    )
    obs = sessao.get("observacao") or "Sem observacao."
    return Table(
        [
            [Paragraph(f"<b>{titulo}</b>", estilos["Normal"])],
            [Paragraph(f"<font color='#525252'>{meta}</font>", estilos["Muted"])],
            [Paragraph(obs, estilos["Normal"])],
        ],
        colWidths=[160 * mm],
        style=TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#d4d4d4")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        ),
    )


def tabela(dados, header=False):
    table = Table(dados, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d4d4d4")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f5f5")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style.append(("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"))
    table.setStyle(TableStyle(style))
    return table
