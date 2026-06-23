from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.tarefa import Tarefa
from app.models.tarefa_db import TarefaDB
from database.db import get_db

router = APIRouter(prefix="/v1/tarefas", tags=["tarefas"])


@router.get("/")
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(TarefaDB).all()


@router.post("/")
def criar_tarefa(tarefa: Tarefa, db: Session = Depends(get_db)):
    nova_tarefa = TarefaDB(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        status=tarefa.status,
        prioridade=tarefa.prioridade,
        data_criacao=datetime.now(),
        data_vencimento=tarefa.data_vencimento,
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa


@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()

    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()
    return {"detail": "Tarefa removida com sucesso"}


@router.put("/{tarefa_id}")
def alterar_tarefa(
    tarefa_id: int, tarefa_atualizada: Tarefa, db: Session = Depends(get_db)
):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()

    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.titulo = tarefa_atualizada.titulo
    tarefa.descricao = tarefa_atualizada.descricao
    tarefa.status = tarefa_atualizada.status
    tarefa.prioridade = tarefa_atualizada.prioridade
    tarefa.data_vencimento = tarefa_atualizada.data_vencimento

    db.commit()
    db.refresh(tarefa)
    return tarefa
