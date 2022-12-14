import pytest
from api import app

@pytest.fixture()
def client():
    return app.test_client()

def test_cadastrar(client):
    resultado = client.get('/cadastrar/?nome=teste&preco=4&quantidade=10')
    client.get('deletar/teste')
    assert resultado.json == {"nome": "teste","preco": "4", "quantidade": "10"}

def test_cadastrar_status(client):
    resultado = client.get('/cadastrar/?nome=teste&preco=4&quantidade=10')
    assert resultado.status_code == 200

def test_read_status(client):
    resultado = client.get('/consultar/')
    assert resultado.status_code == 200

def test_read_content(client):
    resultado = client.get('/consultar/')
    assert resultado.json == [{"nome": "teste","preco": "4","quantidade": "10"}]

def test_read_id_status(client):
    resultado = client.get('/consultar/teste')
    assert resultado.status_code == 200

def test_read_id_content(client):
    resultado = client.get('/consultar/teste')
    assert resultado.json == {"nome": "teste","preco": "4","quantidade": "10"}

def test_update_id_status(client):
    resultado = client.get('/atualizar/?nome=teste&preco=5&quantidade=10')
    assert resultado.status_code == 200

def test_update_id_content(client):
    resultado = client.get('/atualizar/?nome=teste&preco=5&quantidade=10')
    assert resultado.json == {"nome": "teste","preco": "5","quantidade": "10"}

def test_delete_produto_content(client):
    resultado = client.get('/deletar/teste')
    assert resultado.json == { "message": "Produto deletado!" }

def test_delete_produto_status(client):
    client.get('/cadastrar/?nome=teste&preco=4&quantidade=10')
    resultado = client.get('/deletar/teste')
    assert resultado.status_code == 200

def test_delete_tudo_content(client):
    client.get('/cadastrar/?nome=teste&preco=4&quantidade=10')
    resultado = client.get('/deletar/')
    assert resultado.json == {"message": "Banco de dados apagado!"}

def test_delete_tudo_status(client):
    client.get('/cadastrar/?nome=teste&preco=4&quantidade=10')
    resultado = client.get('/deletar/')
    assert resultado.status_code == 200

