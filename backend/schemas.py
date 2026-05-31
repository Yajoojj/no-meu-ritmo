from typing import Literal

from pydantic import BaseModel, Field, field_validator


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
