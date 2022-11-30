from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

#mongopass = os.environ['mongopass']

conn = MongoClient(
    'mongodb+srv://cluster0.bhbsfvp.mongodb.net/test',
    username='canela',
    password='canelagrupo'
)

db = conn['canela']

# Create
#db.create_collection("canelaLoja")
#db.getCollectionNames()

@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))
#@app.route('/cadastrar/', methods=['GET'])
# ?nome=tomate&preco=10

# Read
@app.route('/consultar/')
def consultar():
    cursor = db.produtos.find({}, {'_id':False})
    produtos = list(cursor)
    return produtos

@app.route('/cadastrar/')

def cadastrar():
    produto = request.args.to_dict() #{'nome': 'tomate', 'preco':10}
    print(produto)
    if not produto: #{}
        return redirect(url_for('static', filename='cadastrar.html'))
    else: #{'nome': 'tomate', 'preco':10}
        query = db.produtos.find_one(produto)
        #query = db.produtos.find_one(preco)
        # find => Cursor => list(Cursor) [{}, {}]
        # find_one => {}
        #if query: #tomate está no banco
        if query: #tomate está no banco
            return {'error': 'Produto já cadastrado!'}
        else: # tomate não está no banco
            db.produtos.insert_one(produto)
            del produto['_id']
            return produto   

if __name__ == '__main__':
    app.run(debug=True)
