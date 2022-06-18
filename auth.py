# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # verifique se o usuário realmente existe
    # pegue a senha fornecida pelo usuário, faça um hash e compare-a com
    # a senha com hash no banco de dados
    if not user or not check_password_hash(user.password, password): 
        flash('Por favor, verifique os seus dados de login e tente novamente.')
        return redirect(url_for('auth.login'))
        # se o usuário não existir ou a senha estiver errada,
        # recarregue a página

    # se a verificação acima for aprovada, sabemos que o usuário tem as credenciais corretas
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # se isso retornar um usuário, então o e-mail já existe no banco de dados
    user = User.query.filter_by(email=email).first()

    # se um usuário for encontrado, queremos redirecionar de volta para a página de inscrição
    # para que o usuário possa tentar novamente
    if user:
        flash('Endereço de email já cadastrado')
        return redirect(url_for('auth.signup'))

    # crie um novo usuário com os dados do formulário. Hash a senha para que a versão em
    # texto simples não seja salva.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # adicione o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))