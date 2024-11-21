from flask import Flask
from config.db_setup import init_db 
from routes.app_routes import app_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp   
from routes.address_routes import address_bp  
from routes.institution_routes import institution_bp  
from routes.email_routes import email_bp

app = Flask(__name__)

#Inicialização do banco
init_db()

#Chave para seção
app.secret_key = 'sua-chave-secreta' 

#Rotas da Aplicação
app.register_blueprint(app_bp)

#Rotas de Administrador
app.register_blueprint(admin_bp)

#Rotas para Usuário
app.register_blueprint(user_bp)

#Rotas para Endereço
app.register_blueprint(address_bp)

#Rotas para Instituição
app.register_blueprint(institution_bp)

#Rotas para dominios de email
app.register_blueprint(email_bp)

if __name__ == '__main__':
    app.run(debug=True)

