from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy


class Curso:
    def __init__(self, nome, duracao):
        self.nome = nome
        self.duracao = duracao


curso1 = Curso('HTML+CSS', '20h')
curso2 = Curso('JavaScript Completo', '40h')
curso3 = Curso('React', '16h')
curso4 = Curso('Python', '40h')
curso5 = Curso('AWS', '16h')

list_cursos = [curso1, curso2, curso3, curso4, curso5]

app = Flask(__name__)
app.secret_key = '@admin9876'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{databse}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='cursos'
)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('cursos.html', titulo='Cursos:', cursos=list_cursos)


@app.route('/cadastro')
def cadastro():
    if 'admin_logado' not in session or session['admin_logado'] == None:
        return redirect('/login?proxima=cadastro')
    return render_template('cadastro.html', titulo='Novo Curso')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    duracao = request.form['duracao']
    curso = Curso(nome, duracao)
    list_cursos.append(curso)
    return redirect('/')


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autemticacao():
    if '@admin1234' == request.form['senha'] and 'admin' == request.form['usuario']:
        session['admin_logado'] = request.form['usuario']
        flash(session['admin_logado'] + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Dados incorretos!')
        return redirect('/login')


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')


app.run(debug=True)
