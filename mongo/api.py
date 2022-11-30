from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient

app = Flask(__name__)
#conn = MongoClient('mongodb+srv://username:password@cluster0.rn9t8ag.mongodb.net/magalu'
conn = MongoClient(
    'mongodb+srv://canela:canelagrupo@cluster0.bhbsfvp.mongodb.net/test',
    username='canela',
    password='canelagrupo'
)

db = conn['<canela>']

# Create
#db.create_collection("<canelaLoja>")
#db.getCollectionNames()


@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))
@app.route('/cadastrar/', methods=['GET'])
# ?nome=tomate&preco=10

# Read
@app.route('/consultar/')
def consultar():
    cursor = db.produtos.find({}, {'_id':False})
    produtos = list(cursor)
    return produtos

def cadastrar():
    produto = request.args.to_dict() #{'nome': 'tomate', 'preco':10}
    print(produto)
    if not produto: #{}
        return redirect(url_for('static', filename='cadastrar.html'))
    else: #{'nome': 'tomate', 'preco':10}
        query = db.produtos.find_one({'nome': produto['nome']})
        # find => Cursor => list(Cursor) [{}, {}]
        # find_one => {}
        #if query: #tomate está no banco

if __name__ == '__main__':
    app.run(debug=True)


#mongodb+srv://canela:<canelagrupo>@cluster0.bhbsfvp.mongodb.net/test