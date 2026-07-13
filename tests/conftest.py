import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database.db import Base
from app.models.tarefa_db import TarefaDB
from fastapi.testclient import TestClient
from database.db import get_db
from main import app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def tarefa_criada(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste",
            "descricao": "Deleção de registro válido",
            "status": "pendente",
            "prioridade": "alta",
            "data_vencimento": "2026-12-31",
        },
    )
    return resposta.json()


@pytest.fixture
def usuario_cadastrado(client):
    resposta = client.post(
        "/auth/cadastro", json={"email": "teste@teste.com", "senha": "123456"}
    )
    return resposta.json()


@pytest.fixture
def token_valido(client, usuario_cadastrado):
    resposta = client.post(
        "/auth/login", data={"username": "teste@teste.com", "password": "123456"}
    )
    return resposta.json()["access_token"]
