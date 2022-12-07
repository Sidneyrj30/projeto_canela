import pytest
from app import app

@pytest.fixture()
def client():
    return app.test_client()

def test_adicionar_produto_carrinho_content(client):
    resultado = client.get('/add/?id=100&nome=myproduct&quantidade=25')
    client.get('/delete/100/')
    assert resultado.json == {'id': '100', 'nome': 'myproduct', 'quantidade': '25'}

def test_adicionar_produto_carrinho_status(client):
    resultado = client.get('/add/?id=100&nome=myproduct&quantidade=25')
    assert resultado.status_code == 200

def test_read_status(client):
    resultado = client.get('/read/')
    assert resultado.status_code == 200

def test_read_content(client):
    resultado = client.get('/read/')
    assert resultado.json == [[100, 'myproduct', 25]]

def test_read_id_status(client):
    resultado = client.get('/read/100/')
    assert resultado.status_code == 200

def test_read_id_content(client):
    resultado = client.get('/read/100/')
    assert resultado.json == [[100, 'myproduct', 25]]

def test_update_id_status(client):
    resultado = client.get('/update/100/?id=100&nome=myproduct&quantidade=5')
    assert resultado.status_code == 200

def test_update_id_content(client):
    resultado = client.get('/update/100/?id=100&nome=myproduct&quantidade=5')
    assert resultado.json == { "id": "100", "nome": "myproduct", "quantidade": "5"}

def test_delete_produto_carrinho_content(client):
    resultado = client.get('/delete/100/')
    assert resultado.json == { "message": "1 produto(s) foram removido(s) do carrinho!" }

def test_delete_produto_carrinho_status(client):
    client.get('/add/?id=100&nome=myproduct&quantidade=25')
    resultado = client.get('/delete/100/')
    assert resultado.status_code == 200

def test_delete_tudo_content(client):
    client.get('/add/?id=100&nome=myproduct&quantidade=25')
    resultado = client.get('/delete_all/')
    assert resultado.json == {'message': 'todos os produto(s) foram removido(s) do carrinho!'}

def test_delete_tudo_status(client):
    client.get('/add/?id=100&nome=myproduct&quantidade=25')
    resultado = client.get('/delete_all/')
    assert resultado.status_code == 200

