from flask import Flask
import mysql.connector as sql

app = Flask(__name__)

def abrir_conexao(dicionario=False):
    conexao = sql.connect(
        host="127.0.0.1",
        user="root",
        password="vB?#",
        database="projeto_canela"
    )
    cursor = conexao.cursor(dictionary=dicionario)
    return conexao, cursor

def fechar_conexao(conexao):
    conexao.commit()
    conexao.close()

total_vendas = "SELECT COUNT(nome) as total_produtos, SUM(quantidade) as total_quantidade, ROUND(SUM(preco), 2) as total_preco from VENDAS;"
rank_vendas = "SELECT * FROM VENDAS ORDER BY quantidade DESC;" 

@app.route('/total', methods=["GET"])
def total():
    conexao, cursor = abrir_conexao(True)
    cursor.execute(total_vendas)
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

if __name__ == "__main__":
    app.run(debug=True, port=8000)