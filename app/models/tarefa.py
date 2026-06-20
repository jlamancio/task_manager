from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel

class StatusTarefa(str, Enum):
    pendente = "pendente"
    em_andamento = "em andamento"
    concluida = "concluida"

class PrioridadeTarefa(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"

class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: str | None = None
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media
    data_criacao: datetime
    data_vencimento: date | None = None
    