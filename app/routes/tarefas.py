from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.tarefa import Tarefa, TarefaPatch
from app.services import tarefa_service
from app.dependencies import get_current_user
from database.db import get_db

router = APIRouter(prefix="/v1/tarefas", tags=["tarefas"])


@router.get("/")
def listar_tarefas(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    return tarefa_service.get_tarefas(db)


@router.post("/")
def criar_tarefa(
    tarefa: Tarefa,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return tarefa_service.create_tarefa(tarefa, db)


@router.delete("/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return tarefa_service.delete_tarefa(tarefa_id, db)


@router.put("/{tarefa_id}")
def alterar_tarefa(
    tarefa_id: int,
    tarefa_atualizada: Tarefa,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return tarefa_service.update_tarefa(tarefa_id, tarefa_atualizada, db)


@router.patch("/{tarefa_id}")
def atualizar_parcial(
    tarefa_id: int,
    dados: TarefaPatch,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return tarefa_service.patch_tarefa(tarefa_id, dados, db)
