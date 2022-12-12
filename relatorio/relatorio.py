from flask import Flask, request
import mysql.connector as sql

app = Flask(__name__)

def abrir_conexao(dicionario=False):
    if app.config['TESTING']: #por padrão TESTING=False
        conexao = sql.connect(
        host="127.0.0.1",
        user="root",
        password="Airplanes42",
        database="projeto_canela_teste"
    )
    else:
        conexao = sql.connect(
        host="127.0.0.1",
        user="root",
        password="Airplanes42",
        database="projeto_canela"
        )
    cursor = conexao.cursor(dictionary=dicionario)
    return conexao, cursor

# def abrir_conexao(dicionario=False):
#     conexao = sql.connect(
#         host="127.0.0.1",
#         user="root",
#         password="Airplanes42",
#         database="projeto_canela"
#     )
#     cursor = conexao.cursor(dictionary=dicionario)
#     return conexao, cursor

def fechar_conexao(conexao):
    conexao.commit()
    conexao.close()

total_vendas = "SELECT COUNT(nome) as total_produtos, SUM(quantidade) as total_quantidade, ROUND(SUM(preco), 2) as total_preco from VENDAS;"
rank_vendas = "SELECT * FROM VENDAS ORDER BY quantidade DESC;" 
consulta_vendas = "SELECT * FROM VENDAS;"
rank_10_vendas = "SELECT * FROM VENDAS ORDER BY quantidade DESC LIMIT 10;"
relatorio_vendas = "SELECT * FROM VENDAS"
limpar_vendas = "DELETE FROM VENDAS"
registro_vendas = '''
INSERT INTO VENDAS (nome, preco, descricao, quantidade) VALUES
    (%(nome)s,
    %(preco)s,
    %(descricao)s,
     %(quantidade)s)'''

@app.route('/registro', methods=["POST"])
def registro():
    venda = request.get_json()
    conexao, cursor = abrir_conexao(True)
    cursor.execute(registro_vendas, venda)
    resultado = {"message":"Produto adicionado com sucesso!"}
    fechar_conexao(conexao)
    return resultado  

@app.route('/relatorio', methods=["GET"])
def relatorio():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(relatorio_vendas)
    resultado = cursor.fetchall()
    fechar_conexao(conexao)
    return resultado

@app.route('/rank', methods=["GET"])
def rank():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(rank_vendas)
    resultado = cursor.fetchall() 
    fechar_conexao(conexao)
    return resultado  
 
@app.route('/total', methods=["GET"])
def total():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(total_vendas)
    resultado = cursor.fetchall() 
    fechar_conexao(conexao)
    return resultado  

@app.route('/rank_10', methods=["GET"])
def rank_10():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(rank_10_vendas)
    resultado = cursor.fetchall() 
    fechar_conexao(conexao)
    return resultado 

@app.route('/deleta', methods=["DELETE"])
def deleta():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(limpar_vendas)
    resultado = {'message':'todos os dados foram deletados com sucesso!'}
    fechar_conexao(conexao)
    return resultado

@app.route('/consulta', methods=["GET"])
def consulta():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(consulta_vendas)
    resultado = cursor.fetchall() 
    fechar_conexao(conexao)
    return resultado     

if __name__ == "__main__":
    app.run(debug=True, port=8000)