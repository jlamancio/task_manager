

def test_listar_tarefas_vazias(client):
    resposta = client.get("/v1/tarefas/")

    assert resposta.status_code == 200
    assert resposta.json() == []