from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field


class StatusTarefa(str, Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class PrioridadeTarefa(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class Tarefa(BaseModel):
    id: int | None = None
    titulo: str = Field(min_length=1)  # ADICIONADO: rejeita string vazia (Cypress provou que "" passava antes)
    descricao: str | None = None
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media
    data_criacao: datetime | None = None
    data_vencimento: date


class TarefaPatch(BaseModel):
    titulo: str | None = Field(default=None, min_length=1)  # ADICIONADO: mesma regra, só valida quando o campo é enviado
    descricao: str | None = None
    status: StatusTarefa | None = None
    prioridade: PrioridadeTarefa | None = None
    data_vencimento: date | None = None
