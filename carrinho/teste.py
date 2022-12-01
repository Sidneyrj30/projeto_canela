import sqlite3 as sql

con = sql.connect('carrinho.db')

# Função
# def abrir_conexao(banco):
#     conexao = sql.connect(banco)
#     cursor = conexao.cursor()
#     return conexao, cursor

def fechar_conexao(con):
    con.commit()
    con.close()

cur = con.cursor()
## Criar tabela
# cur.execute('''
# CREATE TABLE produto_carrinho(
#     id INTEGER PRIMARY KEY,
#     nome text,
#     quantidade int
# );
#  ''')
#cur.execute('''INSERT INTO produto_carrinho VALUES (null,'repolho',15)''')
#cur.execute("DELETE FROM produtos WHERE id like 1")

cur.execute('''
    UPDATE produto_carrinho SET
    quantidade = quantidade -1
    WHERE id like 1  
''')
cur.execute("SELECT * FROM produto_carrinho")
print(cur.fetchall())
con.commit()
con.close()




