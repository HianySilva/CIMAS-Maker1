from flask import Blueprint, request, redirect, url_for, send_from_directory, current_app, render_template
import os

# Criando o Blueprint para as rotas da aplicação
app_bp = Blueprint('app', __name__)

# Rota para a página inicial
@app_bp.route('/')
def home():
    return render_template('home.html')  # Certifique-se de que o arquivo existe na pasta templates

# Rota para a página de login
@app_bp.route('/login')
def login():
    return render_template('login.html')

# Rota para a página de registro
@app_bp.route('/register')
def register():
    return render_template('register.html')

@app_bp.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app_bp.route('/projeto', methods=['GET'])
def projeto():
    return render_template('projeto.html')


