from flask import Flask, render_template,request,redirect
import pandas as pd
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

@app.route('/')
def index():
    cart = requests.get('http://127.0.0.1:8080/read/')
    return render_template('home.html', carrinho = cart.json())

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/listar_produtos')
def listar():
    produto = (requests.get(f'http://127.0.0.1:8000/consultar/'))
    return render_template('listar_produtos.html', produtos = produto.json())
    

@app.route('/cadastro')
def cadastro():
   return render_template('cadastro.html')

@app.route('/cadastrar')
def adicionarProduto():
    argumentos = request.args.to_dict()
    quantidade = argumentos['quantidade']
    nome = argumentos['nome']
    preco = argumentos['preco']
    argRequest = requests.get(f'http://127.0.0.1:8000/cadastrar/?nome={nome}&quantidade={quantidade}&preco={preco}')
    return redirect('/cadastro')

@app.route('/deletar/<nome>')
def deletar(nome):
    argRequest = requests.get(f'http://127.0.0.1:8000/deletar/{nome}')

    return redirect('/listar_produtos')

#Vendas carrinho ========================================================  

#pendente
@app.route('/vendas')
def vendas():
    produto = (requests.get(f'http://127.0.0.1:8000/consultar/'))
    cart = requests.get('http://127.0.0.1:8080/read/')
    return render_template('vendas.html', produtos = produto.json(), carrinho = cart.json())

@app.route('/adicionar/<nome>/<preco>')
def adicionarCarrinho(nome,preco):
    argumentos = request.args.to_dict()
    quantidade = int(argumentos['quantidade'])
    cart = requests.get('http://127.0.0.1:8080/read/')
    cart = cart.json()
    verifica_nome = False
    for item in cart:
        if item[1] == nome:
            quantidade_antiga= int(item[2])
            verifica_nome = True
    if verifica_nome == True:
        soma=quantidade+quantidade_antiga
        requests.get(f'http://127.0.0.1:8080/update_nome/{nome}/?nome={nome}&quantidade={soma}')
    else:
        requests.get(f'http://127.0.0.1:8080/add/?nome={nome}&quantidade={quantidade}&preco={preco}')
    return redirect('/vendas')


@app.route('/carrinho')
def carrinho():
    cart = requests.get('http://127.0.0.1:8080/read/')
    total_carrinho = cart.json()
    total=0
    for produto in total_carrinho:
        total = total + (produto[2]*produto[3])
    return render_template('carrinho.html', carrinho = cart.json(),total = total)

@app.route('/deletarCarrinho/<id>')
def deletarCarrinho(id):
    cart = requests.get(f'http://127.0.0.1:8080/delete/{id}/')
    return redirect('/carrinho')

@app.route('/updateCarrinho/<id>/')
def updateCarrinho(id):
    argumentos = request.args.to_dict()
    argumentos= argumentos['quantidade']
    cart = requests.get(f'http://127.0.0.1:8080/update_id/{id}/?id={id}&quantidade={argumentos}')
    return redirect('/carrinho')
    
@app.route('/gerarRelatorio')
def gerarRelatorio():
    cart = requests.get('http://127.0.0.1:8080/read/')

    carrinho_list = cart.json()
    carrinho = pd.DataFrame(carrinho_list, columns= ["id", "nome", "quantidade", "preco"])
    carrinho.drop('id', inplace=True, axis=1)
    carrinho_dict = carrinho.to_dict("records")

    for item in carrinho_dict:
        requests.post("http://127.0.0.1:3000/registro",json = item)

    requests.get('http://127.0.0.1:8080/delete_all') 
    return redirect('/relatorio')

@app.route('/relatorio')
def relatorio():
    url = "http://127.0.0.1:3000/consulta_agrupada"
    response = requests.get(url)
    relatorio = response.json() 
    print(relatorio) 
    total = 0
    for produto in relatorio:
        total = total + produto["total"]
    return render_template('relatorio.html', relatorio = relatorio,total=total) 

if __name__ == '__main__':
    app.run(app.run(port=8085, host='0.0.0.0', debug=True))