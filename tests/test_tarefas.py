from app import app


def test_tarefas():
    cliente = app.test_client()

    resposta = cliente.get("/tarefas")

    assert resposta.status_code == 200