def test_listar_tarefas_vazias(client):
    resposta = client.get("/v1/tarefas/")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_adicionar_tarefas(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Incluir atividades de construção do backend",
            "status": "pendente",
            "prioridade": "alta",
            "descricao": "Teste de inclusão de tarefa via método POST",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Incluir atividades de construção do backend"
    assert resposta.json()["id"] == 1


def test_adicionar_tarefa_sem_titulo(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "status": "pendente",
            "prioridade": "alta",
            "descricao": "Teste de inclusão de tarefa via método POST",
            "data_vencimento": "2026-12-31",
        },
    )

    assert resposta.status_code == 422
    assert resposta.json()


def test_adicionar_tarefa_sem_data_vencimento(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Incluir atividades de construção do backend",
            "status": "pendente",
            "prioridade": "alta",
            "descricao": "Teste de inclusão de tarefa via método POST",
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()


def test_adicionar_tarefa_status_invalido(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Incluir atividades de construção do backend",
            "status": "invalido",
            "prioridade": "alta",
            "descricao": "Teste de inclusão de tarefa via método POST",
            "data_vencimento": "2026-12-31",
        },
    )
  
    assert resposta.status_code == 422
    assert resposta.json()


def test_adicionar_tarefa_prioridade_invalida(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Incluir atividades de construção do backend",
            "status": "pendente",
            "prioridade": "inválida",
            "descricao": "Teste de inclusão de tarefa via método POST",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()
    
