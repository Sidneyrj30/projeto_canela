from flask import Flask, render_template,request,redirect, flash
import pandas as pd
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

df = pd.read_json('data.json')
produtos = df.to_dict('records')

Carrinho = pd.DataFrame([])
Relatorio = pd.DataFrame([])

@app.route('/')
def index():
    return render_template('home.html', carrinho = Carrinho.to_dict('records'))

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/listar_produtos')
def listar():
    global df
    df = pd.read_json('data.json')
    return render_template('listar_produtos.html', produtos = df.to_dict('records'), carrinho = Carrinho.to_dict('records') )

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', carrinho = Carrinho.to_dict('records'))

@app.route('/cadastrado')#/adicionar?produto=valor&preco=valor
def cadastrado():
    global df
    argumentos = request.args.to_dict(True)
    #print(argumentos)
    if df.empty:
        argumentos['id'] = [1]
    else:
        argumentos['id'] = [df['id'].max() + 1]
    df = pd.concat([df, pd.DataFrame(argumentos)], ignore_index=True)
    df.to_json('data.json', orient='records')
    return redirect('/cadastro')

@app.route('/deletar/<id>')
def deletar(id):
    mask_id = df[df['id'] == int(id)].index
    df.drop(mask_id, axis=0, inplace=True)
    df.to_json('data.json', orient='records')
    return redirect('/listar_produtos')

#Vendas carrinho ========================================================  

#pendente
@app.route('/vendas')
def vendas():
    global df
    df = pd.read_json('data.json')
    return render_template('/vendas.html', produtos = df.to_dict('records'), carrinho = Carrinho.to_dict('records'))

@app.route('/adicionar/<id>/<nome>/<preco>')
def adicionarCarrinho(id,nome,preco):
    argumentos = request.args.to_dict()
    print('print dos argumentos' ,argumentos)
    quantidade = argumentos['quantidade']
    # preco = argumentos['preco']
    cart = requests.get(f'http://127.0.0.1:5000/add/?id={id}&nome={nome}&quantidade={quantidade}&preco={preco}')
    return redirect('/vendas')


@app.route('/carrinho')
def carrinho():
    cart = requests.get('http://127.0.0.1:5000/read/')
    return render_template('carrinho.html', cart = cart.json())

@app.route('/deletarCarrinho/<id>')
def deletarCarrinho(id):
    cart = requests.get(f'http://127.0.0.1:5000/delete/{id}/')
    return redirect('/carrinho')

@app.route('/updateCarrinho/<id>/')
def updateCarrinho(id):
    argumentos = request.args.to_dict()
    argumentos= argumentos['quantidade']
    cart = requests.get(f'http://127.0.0.1:5000/update/{id}/?id={id}&quantidade={argumentos}')
    return redirect('/carrinho')
    

@app.route('/gerarRelatorio')
def gerarRelatorio():
    global Relatorio
    global Carrinho
    carrinho_dict = Carrinho.to_dict('records')
    if Relatorio.empty:
     Relatorio = pd.concat([Relatorio, Carrinho])
    else:
        for produto in carrinho_dict:
            resultado = Relatorio['nome'] == produto['nome']
            if Relatorio[resultado].empty:
                print("Não tem!")
                Relatorio = pd.concat([Relatorio, pd.DataFrame(produto, index=[0])], ignore_index=True) #sem o index =[0] da erro
            else:
                print("Ok, esse existe")
                Relatorio.loc[resultado, "quantidade"] = Relatorio[resultado]["quantidade"].values[0] + produto['quantidade']  
    Carrinho = pd.DataFrame([]) 
    # global Relatorio
    # global Carrinho
    # Relatorio = pd.concat([Relatorio, Carrinho.copy()])
    # Carrinho = pd.DataFrame([])
    # print(Relatorio)
    return redirect('/carrinho')
#=====================================================

@app.route('/relatorio')
def relatorio():
    global Relatorio
    relatorio_dict = Relatorio.to_dict('records')
    total = 0
    for produto in relatorio_dict:
        total = total + produto["quantidade"] * produto["preco"]
    return render_template('relatorio.html', 
    relatorio = Relatorio.to_dict('records'), carrinho = Carrinho.to_dict('records'),
    total=total) 

if __name__ == '__main__':
    app.run(app.run(port=8085, host='0.0.0.0', debug=True))