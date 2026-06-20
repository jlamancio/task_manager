from datetime import datetime
from fastapi import APIRouter
from app.models.tarefa import Tarefa

router = APIRouter(prefix="/v1/tarefas", tags=["Tarefas"])

tarefas_db: list[Tarefa] = []


@router.get("/")
def listar_tarefas():
    return tarefas_db


@router.post("/")
def criar_tarefa(tarefa: Tarefa):
    tarefa.data_criacao = datetime.now()
    tarefas_db.append(tarefa)
    return tarefa