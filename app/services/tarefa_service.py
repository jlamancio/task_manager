from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.tarefa import Tarefa, TarefaPatch
from app.models.tarefa_db import TarefaDB


def get_tarefas(db: Session):
    return db.query(TarefaDB).all()


def create_tarefa(tarefa: Tarefa, db: Session):
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


def delete_tarefa(tarefa_id: int, db: Session):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()

    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()
    return {"detail": "Tarefa removida com sucesso"}


def update_tarefa(tarefa_id: int, tarefa_atualizada: Tarefa, db: Session):
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


def patch_tarefa(tarefa_id: int, dados: TarefaPatch, db: Session):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()

    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    dados_enviados = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_enviados.items():
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)
    return tarefa
