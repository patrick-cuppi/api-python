from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = '@admin9876'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='cursos'
)

db = SQLAlchemy(app)


class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    duracao = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


# class adm(db.Model):
#    nome = db.Column(db.String(20), nullable=False)
#    senha = db.Column(db.String(100), nullable=False)
#
#    def __repr__(self):
#        return '<Name %r>' % self.name


@app.route('/')
def index():
    lista = Cursos.query.order_by(Cursos.id)
    return render_template('cursos.html', titulo='Cursos:', cursos=lista)


@app.route('/cadastro')
def cadastro():
    if 'admin_logado' not in session:
        return redirect('/login?proxima=cadastro')
    return render_template('cadastro.html', titulo='Novo Curso')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    duracao = request.form['duracao']
    curso = Cursos.query.filter_by(nome=nome).first()
    if curso:
        flash('Curso já existente!')
        return redirect('/')
    novo_curso = Cursos(nome=nome, duracao=duracao)
    db.session.add(novo_curso)
    db.session.commit()

    return redirect('/')


@app.route('/editar/<int:id>')
def editar(id):
    if 'admin_logado' not in session:
        return redirect('/login?proxima=editar')
    curso = Cursos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Curso', curso=curso)


@app.route('/atualizar', methods=['PUT', ])
def atualizar():
    curso = Cursos.query.filter_by(id=request.form['id']).first()
    curso.nome = request.form['nome']
    curso.duracao = request.form['duracao']

    db.session.add(curso)
    db.session.commit()
    return redirect('/')


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'admin_logado' not in session:
        return redirect('/login')

    Cursos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Curso deletado com sucesso!')
    return redirect('/')


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticacao():
    if 'admin' == request.form['senha']:
        session['admin_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Usuário não logado.')
        return redirect('/login')


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
