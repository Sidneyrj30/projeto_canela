from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as sql

app = Flask(__name__)
banco = 'carrinho.db'

# Função
def abrir_con(banco):
    con = sql.connect(banco)
    cur = con.cursor()
    return con, cur

def fechar_con(con):
    con.commit()
    con.close()

 #id,nome,quantidade
# Comandos SQL
contagem = "SELECT COUNT(*) FROM produto_carrinho;"
select_todos = "SELECT * FROM produto_carrinho;"
truncate = "DELETE FROM produto_carrinho;" #"TRUNCATE TABLE produto_carrinho;"

select_id = "SELECT * FROM produto_carrinho WHERE id like ?"
delete_id = "DELETE FROM produto_carrinho WHERE id like ?"
insert = "INSERT INTO produto_carrinho VALUES (null, :nome, :quantidade)"
update = '''
UPDATE produto_carrinho SET
    id = :id,
    quantidade = :quantidade
WHERE id like :id 
'''

# Adição de produtos
@app.route('/adicionar')
#?id=1&nome=banana&quantidade=quantidade-1
def adicionar_produto_carrinho():
    produto=request.args.to_dict() #{chave: valor, chave:valor,...}
    if produto: # se tem argumento
        con, cur = abrir_con(banco)
        cur.execute(insert, produto)
        fechar_con(con)
        return produto
    else: # se não tem argumento
        return {'error': 'solicitação sem argumentos!'}

# Remoção de produtos
@app.route('/delete/<id>')
def delete_produto_carrinho(id):
    con, cur = abrir_con(banco)
    resultado = cur.execute(delete_id, [id]).rowcount
    fechar_con(con)
    return {'message': f'{resultado} produto(s) foram removido(s) do carrinho!'}

# Alteração de quantidade
#?id=1&nome=banana&quantidade=12
# update
@app.route('/update/<id>/')
def update_id(id):
    consulta = read_id(id)
    if consulta: # existe nome no banco de dados
        produto=request.args.to_dict() #{chave: valor, chave:valor,...}
        print(produto)
        if produto: # se tem argumento
            con, cur = abrir_con(banco)
            cur.execute(update, produto)
            fechar_con(con)
            return produto
        else: # se não tem argumento
            return render_template('atualizacao.html', produto=consulta[0])
    else: # não existe nome no banco de dados
        return {'error': 'produto não encontrado!'}

# Consulta de itens
# read por id
# read all
@app.route('/read')
def read():
    con, cur = abrir_con(banco)
    resultado = cur.execute(select_todos).fetchall()
    fechar_con(con)
    return resultado

@app.route('/read/<id>')
def read_id(id):
    con, cur = abrir_con(banco)
    resultado = cur.execute(select_id, [id]).fetchall()
    fechar_con(con)
    return resultado

# # index
# @app.route('/')
# def index():
#     con, cur = abrir_con(banco)
#     resultado = cur.execute(contagem).fetchone()
#     fechar_con(con)
#     return {'registros': f'{resultado[0]} produto_carrinho'}

# # read all
# @app.route('/read')
# def read():
#     con, cur = abrir_con(banco)
#     resultado = cur.execute(select_todos).fetchall() #[(produto1, ...), (produto2, ...)]
#     fechar_con(con)
#     return resultado

# # read por nome
# @app.route('/read/<nome>')
# def read_name(nome):
#     con, cur = abrir_con(banco)
#     resultado = cur.execute(select_nome, [nome]).fetchall()
#     fechar_con(con)
#     return resultado

# # create
# @app.route('/create')
# #?id=1&nome=banana&quantidade=quantidade-1
# def create():
#     produto=request.args.to_dict() #{chave: valor, chave:valor,...}
#     if produto: # se tem argumento
#         con, cur = abrir_con(banco)
#         cur.execute(insert, produto)
#         fechar_con(con)
#         return produto
#     else: # se não tem argumento
#         return redirect(url_for('static', filename='cadastro.html'))

# # delete nome
# @app.route('/delete/<nome>')
# def delete_name(nome):
#     con, cur = abrir_con(banco)
#     resultado = cur.execute(delete_nome, [nome]).rowcount
#     fechar_con(con)
#     return {'message': f'{resultado} produto(s) foram removido(s)!'}

# # delete all
# @app.route('/delete')
# def delete_all():
#     con, cur = abrir_con(banco)
#     cur.execute(truncate)
#     fechar_con(con)
#     return {'message': 'Todos os produto_carrinho foram apagados!'}

# # update
# @app.route('/update/<nome>')
# #?nome=teste&idade=0&filhos=1&estado=AC&altura=0.07&formacao=Ensino+Superior
# def update_name(nome):
#     consulta = read_name(nome)
#     if consulta: # existe nome no banco de dados
#         produto=request.args.to_dict() #{chave: valor, chave:valor,...}
#         if produto: # se tem argumento
#             con, cur = abrir_con(banco)
#             cur.execute(update, produto)
#             fechar_con(con)
#             return produto
#         else: # se não tem argumento
#             return render_template('atualizacao.html', produto=consulta[0])
#     else: # não existe nome no banco de dados
#         return {'error': 'produto não encontrado!'}


if __name__ == "__main__":
    app.run(debug=True)