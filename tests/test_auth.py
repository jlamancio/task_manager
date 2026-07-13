from datetime import timedelta
from app.services.auth_service import criar_token




def test_cadastrar_usuario_valido(client):
    resposta = client.post(
        "/auth/cadastro", json={"email": "novo@teste.com", "senha": "123456"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["email"] == "novo@teste.com"
    assert "senha_hash" not in resposta.json()

def test_cadastrar_emaill_duplicado(client):
    client.post("/auth/cadastro", json={
        "email": "duplicado@teste.com",
        "senha": "123456",
    })
    
    resposta = client.post("/auth/cadastro", json={
        "email": "duplicado@teste.com",
        "senha": "123456",
    })

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Email já cadastrado"

def test_cadastrar_sem_email(client):
    resposta = client.post("/auth/cadastro", json={
        "senha": "123456",
    })
    assert resposta.status_code == 422


def test_cadastrar_sem_senha(client):
    resposta = client.post("/auth/cadastro", json={
        "email": "teste@teste.com",
    })
    assert resposta.status_code == 422


def test_login_valido(client, usuario_cadastrado):
    resposta = client.post("/auth/login", data={
        "username": "teste@teste.com",
        "password": "123456",
    })
    assert resposta.status_code == 200
    assert "access_token" in resposta.json()
    assert resposta.json()["token_type"] == "bearer"


def test_login_com_email_inexistente(client, usuario_cadastrado):
    resposta = client.post("/auth/login", data={
        "username": "inexistente@teste.com",
        "password": "123456",
    })
    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Email ou senha inválidos"

def test_login_com_senha_invalida(client, usuario_cadastrado):
    resposta = client.post("/auth/login", data={
        "username": "teste@teste.com",
        "password": "invalida",
    })
    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Email ou senha inválidos"

def test_login_sem_username(client):                           
    resposta = client.post("/auth/login", data={
        "password": "123456",
    })
    assert resposta.status_code == 422

def test_login_sem_password(client):
    resposta = client.post("/auth/login", data={
        "username": "teste@teste.com",
    })
    assert resposta.status_code == 422

def test_acessar_tarefas_com_token_valido(client, token_valido):
    headers = {"Authorization": f"Bearer {token_valido}"}
    resposta = client.get("/v1/tarefas/", headers=headers)
    assert resposta.status_code == 200 

def test_acessar_tarefas_sem_token(client):
    resposta = client.get("/v1/tarefas/")
    assert resposta.status_code == 401

def test_acessar_tarefas_com_token_invalido(client):
    headers = { "Authorization": "Bearer token_invalido"}
    resposta = client.get("/v1/tarefas/", headers=headers)
    assert resposta.status_code == 401

def test_acessar_tarefa_com_token_expirado(client, usuario_cadastrado):
    token_expirado = criar_token(
        {"sub": "teste@teste.com"},
        expires_delta = timedelta(minutes = -1)
    )
    headers = { "Authorization": f'Bearer {token_expirado}'}
    resposta = client.get("/v1/tarefas/", headers=headers)
    assert resposta.status_code == 401

def test_senha_hash_nao_aparece_no_cadastro(client):
    resposta = client.post("/auth/cadastro", json={
        "email": "seguranca@teste.com",
        "senha": "123456",
    })
    assert resposta.status_code == 200 
    assert "senha_hash" not in resposta.json()
    assert "senha" not in resposta.json()

def test_mensagem_erro_login_generica(client, usuario_cadastrado):
    resposta_email = client.post("/auth/login", data={
        "username": "email_inexistente@teste.com",
        "password": "123456",
    })
    resposta_senha = client.post("/auth/login", data={
        "username": "teste@teste.com",
        "password": "senha_errada"
    })
    assert resposta_email.json()["detail"] == resposta_senha.json()["detail"]