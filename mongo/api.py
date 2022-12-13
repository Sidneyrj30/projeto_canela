from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient

app = Flask(__name__)

conn = MongoClient(
    'mongodb+srv://cluster0.bhbsfvp.mongodb.net/test',
    username='canela',
    password='canelagrupo'
)

db = conn['canela']

# Create
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))


#Cadastrar
@app.route('/cadastrar/', methods=['GET'])
def cadastrar():
    produto = request.args.to_dict()
    print(produto)
    if not produto: #{}
        return redirect(url_for('static', filename='cadastrar.html'))
    else:
        query = db.produtos.find_one({'nome': produto['nome']})
        if query:
            return {'error': 'Produto já cadastrado!'}
        else: 
            db.produtos.insert_one(produto)
            del produto['_id']
            return produto   
# Read
@app.route('/consultar/')
def consultar():
    cursor = db.produtos.find({}, {'_id':False})
    produtos = list(cursor)
    return produtos

# Consultar
@app.route('/consultar/<nome>')
def consultar_nome(nome):
    produto = db.produtos.find_one({'nome': nome}, {'_id':False})
    print(produto)
    if produto: #tomate está no banco
        return produto
    else: # tomate não está no banco
        return {'error': 'Produto não encontrado!'}

@app.route('/atualizar/')
def atualizar():
    produto = request.args.to_dict()
    print(produto)
    if not produto:
        produtos = consultar()
        print(produtos)
        return render_template('atualizar.html', produtos=produtos)
    else: 
        db.produtos.update_one(
            {'nome': produto['nome']},
            {'$set':
                {'preco': produto['preco']}
            }
        )
        return produto

# Deletar 
@app.route('/deletar/<nome>', methods=['GET'])
def deletar_nome(nome):
    produtos = consultar_nome(nome)
    print(produtos)
    if 'error' in produtos:
        return produtos
    else:
        produto =  db.produtos.delete_one({'nome': nome})
        return {'message': 'Produto deletado!'}
    return render_template('deletar.html', produtos=produtos)
   
   # if produto: #tomate está no banco
       # db.produtos.delete_one({'nome': nome})
        #return {'message': 'Produto deletado com sucesso!'}
   # else: # tomate não está no banco
        #return {'error': 'Produto não encontrado!'}

@app.route('/deletar/')
def deletar():
    db.produtos.drop()
    return {'message': 'Banco de dados apagado!'}

if __name__ == '__main__':
    app.run(app.run(port=8000, host='0.0.0.0', debug=True))
