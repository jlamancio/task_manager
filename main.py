from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tarefas, auth
from database.db import Base, engine  # ADICIONADO: necessário para criar as tabelas automaticamente
from app.models import tarefa_db, usuario_db  # ADICIONADO: precisa importar os modelos para o Base "enxergar" as tabelas TarefaDB/UsuarioDB


Base.metadata.create_all(bind=engine)  # ADICIONADO: cria as tabelas que faltarem no startup. É idempotente — se já existem, não mexe em nada (não apaga, não recria, não toca nos dados)

app = FastAPI(title="Task Manager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tarefas.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Task Manager API está no ar!"}