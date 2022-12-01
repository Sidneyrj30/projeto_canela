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
        #query = db.produtos.find_one(produto)
        if query: #tomate está no banco
            return {'error': 'Produto já cadastrado!'}
        else: # tomate não está no banco
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
    produto = request.args.to_dict() #{'nome': 'tomate', 'preco':10}
    print(produto)
    if not produto: #{}
        produtos = consultar()
        print(produtos)
        return render_template('atualizar.html', produtos=produtos)
    else: #{'nome': 'tomate', 'preco':10}
        db.produtos.update_one(
            {'nome': produto['nome']},
            {'$set':
                {'preco': produto['preco']}
            }
        )
        return produto

if __name__ == '__main__':
    app.run(debug=True)
