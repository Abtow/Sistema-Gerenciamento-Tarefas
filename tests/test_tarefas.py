from src.app import app


def test_dashboard():

    cliente = app.test_client()

    resposta = cliente.get("/login")

    assert resposta.status_code == 200