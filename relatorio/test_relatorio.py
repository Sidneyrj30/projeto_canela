from relatorio import app
import pytest

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_total_text(client):
    response = client.get("/total")
    assert "sgngnsgns" not in response.text
    assert "total_preco" in response.text

def test_total_status(client):
    response = client.get("/total")
    assert response.status_code == 200

def test_rank_status(client):
    response = client.get("/rank")
    assert response.status_code == 200

def test_rank_desc(client):
    response = client.get("/rank")
    assert response.json[0]["quantidade"] >= response.json[1]["quantidade"]

def test_rank_10_len(client):
    response = client.get("/rank_10")
    assert len(response.json) <= 10

def test_rank_10_desc(client):
    response = client.get("/rank_10")
    assert response.json[0]["quantidade"] >= response.json[1]["quantidade"]

def test_consulta_status(client):
    response = client.get("/consulta")
    assert response.status_code == 200

def test_consulta_colunas(client):
    response = client.get("/consulta")
    colunas = [ "nome", "preco", "descricao", "quantidade"]
    for coluna in colunas:
        assert coluna in response.json[0].keys()
      
# import requests

# def test_total():
#     headers = {
#         "Accept" : "*/*",
#         "User-Agent" : "request",
#     }
 
#     url= "http://127.0.0.1:8000/total"
#     resposta = requests.get(url, headers=headers)
#     resposta_dict = resposta.json()

#     status = resposta.status_code
#     tamanho_lista = len(resposta_dict)

#     assert status == 200 and tamanho_lista > 0