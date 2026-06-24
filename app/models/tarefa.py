from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel


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
    titulo: str
    descricao: str | None = None
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media
    data_criacao: datetime
    data_vencimento: date 


class TarefaPatch(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    status: StatusTarefa | None = None
    prioridade: PrioridadeTarefa | None = None
    data_vencimento: date | None = None
