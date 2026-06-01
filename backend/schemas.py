from typing import Literal

from pydantic import BaseModel, Field, field_validator


class MateriaEntrada(BaseModel):
    nome: str = Field(..., min_length=2, max_length=80)
    prioridade: Literal["baixa", "media", "alta"] = "media"
    cor: str = Field(default="#2563eb", pattern=r"^#[0-9A-Fa-f]{6}$")
    descricao: str | None = Field(default=None, max_length=240)

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("Informe uma materia.")
        return valor

    @field_validator("descricao")
    @classmethod
    def descricao_limpa(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None


class SessaoEstudoEntrada(BaseModel):
    materia: str = Field(..., min_length=2, max_length=80)
    tipo_estudo: Literal["leitura", "revisao", "exercicios", "projeto"]
    duracao_minutos: int = Field(..., gt=0, le=300)
    nivel_foco: int = Field(..., ge=1, le=5)
    observacao: str | None = Field(default=None, max_length=240)

    @field_validator("materia")
    @classmethod
    def materia_nao_pode_ser_vazia(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("Informe uma matéria.")
        return valor

    @field_validator("observacao")
    @classmethod
    def observacao_limpa(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None
