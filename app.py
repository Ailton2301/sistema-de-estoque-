from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile = db.Column(db.String(20), nullable=False)  # 'admin' ou 'comum'

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_minima = db.Column(db.Integer, nullable=False)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def criar_admin():
    with app.app_context():
        
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            
            admin = Usuario(
                username='admin',
                password=hash_password('admin123'),  # Senha criptografada
                profile='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário administrador criado com sucesso!")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and verify_password(usuario.password, password):
            session['usuario_id'] = usuario.id
            session['profile'] = usuario.profile
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html')


@app.route('/main')
def main():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    return render_template('main.html', profile=session['profile'])


@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if 'usuario_id' not in session or session['profile'] != 'admin':
        flash('Acesso negado!', 'error')
        return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile = request.form['profile']

        if username and password and profile:
            hashed_password = hash_password(password)
            novo_usuario = Usuario(username=username, password=hashed_password, profile=profile)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Todos os campos são obrigatórios!', 'error')

    return render_template('cadastro_usuario.html')


@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        quantidade_minima = request.form['quantidade_minima']

        if nome and quantidade and quantidade_minima:
            try:
                quantidade = int(quantidade)
                quantidade_minima = int(quantidade_minima)
                novo_produto = Produto(nome=nome, quantidade=quantidade, quantidade_minima=quantidade_minima)
                db.session.add(novo_produto)
                db.session.commit()
                flash('Produto cadastrado com sucesso!', 'success')
                return redirect(url_for('main'))
            except ValueError:
                flash('Quantidade e quantidade mínima devem ser números!', 'error')
        else:
            flash('Todos os campos são obrigatórios!', 'error')

    return render_template('cadastro_produto.html')


@app.route('/visualizar_produtos')
def visualizar_produtos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    produtos = Produto.query.all()
    return render_template('visualizar_produtos.html', produtos=produtos)


@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    
    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        
        produto.nome = request.form['nome']
        produto.quantidade = int(request.form['quantidade'])
        produto.quantidade_minima = int(request.form['quantidade_minima'])

        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('visualizar_produtos'))

    
    return render_template('editar_produto.html', produto=produto)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()
        
        criar_admin()
    app.run(debug=True)