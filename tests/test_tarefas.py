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


def test_atualizar_tarefa_existente_com_campos_validos(client):
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
    assert resposta.json()

    resposta = client.put(
        "/v1/tarefas/1",
        json={
            "titulo": "Executado put no título",
            "descricao": "Alteração de campo válido via método PUT",
            "status": "pendente",
            "prioridade": "alta",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Executado put no título"


def test_atualizar_tarefa_existente_com_id_invalido(client):
    resposta = client.put(
        "/v1/tarefas/999",
        json={
            "titulo": "Executado put no título",
            "descricao": "Dependency injection",
            "status": "pendente",
            "prioridade": "media",
            "descricao": "Teste de alteração de tarefa via método PUT",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 404
    assert resposta.json()


def test_atualizar_tarefa_sem_informar_campo_obrigatorio(client):
    resposta = client.put(
        "/v1/tarefas/5",
        json={
            "descricao": "Dependency injection",
            "status": "pendente",
            "prioridade": "media",
            "descricao": "Teste de alteração de tarefa via método PUT",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()


def test_atualizar_tarefa_existente_com_status_invalido(client):
    resposta = client.put(
        "/v1/tarefas/4",
        json={
            "titulo": "Executado put com status invalido",
            "descricao": "Dependency injection",
            "status": "invalido",
            "prioridade": "media",
            "descricao": "Teste de alteração de tarefa via método PUT",
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()
'''
 ----------------------- aqui começa o patch --------------------------------------------------------------------------
'''

def test_atualizar_tarefa_existente_parcialmente_somente_um_campo(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Patch", 
            "descricao": "Atualizacao parcial de registro",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/1",
        json={
            "prioridade": "media"
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["prioridade"] == "media"


def test_atualizar_tarefa_existente_parcialmente_varios_campos(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Patch", 
            "descricao": "Atualizacao parcial de registro",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/1",
        json={
            "titulo": "Alteracao parcial de varios campos obrigatórios", 
            "prioridade": "baixa",
            "data_vencimento": "2027-01-15",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Alteracao parcial de varios campos obrigatórios"
    assert resposta.json()["prioridade"] == "baixa"
    assert resposta.json()["data_vencimento"] == "2027-01-15"

    
def test_atualizar_tarefa_existente_parcialmente_corpo_vazio(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Enviado PATCH com corpo vazio", 
            "descricao": "Atualizacao parcial de registro",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/1",
        json={
         
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

def test_atualizar_tarefa_existente_parcialmente_id_invalido(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Patch", 
            "descricao": "Atualizacao parcial de registro",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/10",
        json={
            "prioridade": "media"
        },
    )
    assert resposta.status_code == 404
    assert resposta.json()

def test_atualizar_tarefa_existente_parcialmente_Enum_invalido(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Patch", 
            "descricao": "Atualizacao parcial de registro",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/1",
        json={
            "status": "status_invalido"
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()


def test_deletar_tarefa_existente(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Delete", 
            "descricao": "Deleção de registro válido",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.delete(
        "/v1/tarefas/1"
    )
    assert resposta.status_code == 200
    assert resposta.json()

def test_deletar_tarefa_existente_id_invalido(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Delete com id invalido", 
            "descricao": "Deleção de registro válido",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.delete(
        "/v1/tarefas/999"
    )
    assert resposta.status_code == 404
    assert resposta.json()


def test_deletar_tarefa_existente_ja_deletada(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Delete", 
            "descricao": "Deleção de registro válido",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.delete(
        "/v1/tarefas/1"
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.delete(
        "/v1/tarefas/1"
    )
    assert resposta.status_code == 404
    assert resposta.json()

def test_fluxo_completo_crud(client):
    resposta = client.post(
        "/v1/tarefas/",
        json={
            "titulo": "Criacao de registro para teste do método Delete", 
            "descricao": "Deleção de registro válido",
            "status": "pendente", 
            "prioridade": "alta", 
            "data_vencimento": "2026-12-31",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.get(
        "/v1/tarefas/",
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client.patch(
        "/v1/tarefas/1",
        json={
            "titulo": "Alteracao parcial fluxo completo - CRUD", 
            "prioridade": "baixa",
 
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Alteracao parcial fluxo completo - CRUD"
    assert resposta.json()["prioridade"] == "baixa"

    
    resposta = client.get(
        "/v1/tarefas/",
    )

    
    resposta = client.delete(
        "/v1/tarefas/1",
    )
