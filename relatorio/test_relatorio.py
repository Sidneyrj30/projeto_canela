import requests
import pytest

def test_total():
    headers = {
        "Accept" : "*/*",
        "User-Agent" : "request",
    }
 
    url= "http://127.0.0.1:8000/total"
    resposta = requests.get(url, headers=headers)
    resposta_dict = resposta.json()

    status = resposta.status_code
    tamanho_lista = len(resposta_dict)

    assert status == 200 and tamanho_lista > 0