def test_listar_tarefas_vazias(client_autenticado):
    resposta = client_autenticado.get("/v1/tarefas/")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_adicionar_tarefas(client_autenticado):
    resposta = client_autenticado.post(
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


def test_adicionar_tarefa_sem_titulo(client_autenticado):
    resposta = client_autenticado.post(
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


def test_adicionar_tarefa_sem_data_vencimento(client_autenticado):
    resposta = client_autenticado.post(
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


def test_adicionar_tarefa_status_invalido(client_autenticado):
    resposta = client_autenticado.post(
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


def test_adicionar_tarefa_prioridade_invalida(client_autenticado):
    resposta = client_autenticado.post(
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


def test_atualizar_tarefa_existente_com_campos_validos(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.put(
        f"/v1/tarefas/{tarefa_id}",
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


def test_atualizar_tarefa_existente_com_id_invalido(client_autenticado):
    resposta = client_autenticado.put(
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


def test_atualizar_tarefa_sem_informar_campo_obrigatorio(client_autenticado):
    resposta = client_autenticado.put(
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


def test_atualizar_tarefa_existente_com_status_invalido(client_autenticado):
    resposta = client_autenticado.put(
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


def test_atualizar_tarefa_existente_parcialmente_somente_um_campo(
    client_autenticado, tarefa_criada
):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.patch(
        f"/v1/tarefas/{tarefa_id}",
        json={"prioridade": "media"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["prioridade"] == "media"


def test_atualizar_tarefa_existente_parcialmente_varios_campos(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.patch(
        f"/v1/tarefas/{tarefa_id}",
        json={
            "titulo": "Alteracao parcial de varios campos obrigatórios",
            "prioridade": "baixa",
            "data_vencimento": "2027-01-15",
        },
    )
    assert resposta.status_code == 200
    assert (
        resposta.json()["titulo"] == "Alteracao parcial de varios campos obrigatórios"
    )
    assert resposta.json()["prioridade"] == "baixa"
    assert resposta.json()["data_vencimento"] == "2027-01-15"


def test_atualizar_tarefa_existente_parcialmente_corpo_vazio(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.patch(
        f"/v1/tarefas/{tarefa_id}",
        json={},
    )
    assert resposta.status_code == 200
    assert resposta.json()


def test_atualizar_tarefa_existente_parcialmente_id_invalido(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.patch(
        "/v1/tarefas/999",
        json={"prioridade": "media"},
    )
    assert resposta.status_code == 404
    assert resposta.json()


def test_atualizar_tarefa_existente_parcialmente_Enum_invalido(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.patch(
        f"/v1/tarefas/{tarefa_id}",
        json={"status": "status_invalido"},
    )
    assert resposta.status_code == 422
    assert resposta.json()


def test_deletar_tarefa_existente(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.delete(f"/v1/tarefas/{tarefa_id}")
    assert resposta.status_code == 200
    assert resposta.json()


def test_deletar_tarefa_existente_id_invalido(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.delete(f"/v1/tarefas/999")
    assert resposta.status_code == 404
    assert resposta.json()


def test_deletar_tarefa_existente_ja_deletada(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.delete(f"/v1/tarefas/{tarefa_id}")
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client_autenticado.delete(f"/v1/tarefas/{tarefa_id}")
    assert resposta.status_code == 404
    assert resposta.json()


def test_fluxo_completo_crud(client_autenticado, tarefa_criada):
    tarefa_id = tarefa_criada["id"]

    resposta = client_autenticado.get(
        "/v1/tarefas/",
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client_autenticado.patch(
        f"/v1/tarefas/{tarefa_id}",
        json={
            "titulo": "Alteracao parcial fluxo completo - CRUD",
            "prioridade": "baixa",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Alteracao parcial fluxo completo - CRUD"
    assert resposta.json()["prioridade"] == "baixa"

    resposta = client_autenticado.get(
        "/v1/tarefas/",
    )
    assert resposta.status_code == 200
    assert resposta.json()

    resposta = client_autenticado.delete(f"/v1/tarefas/{tarefa_id}")
    assert resposta.status_code == 200

    resposta = client_autenticado.get(
        "/v1/tarefas/",
    )
    assert resposta.status_code == 200
    assert resposta.json() == []
