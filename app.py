from flask import Flask
from routes.app_routes import app_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp   


app = Flask(__name__)

#Chave para seção
app.secret_key = 'sua-chave-secreta' 

#Rotas da Aplicação
app.register_blueprint(app_bp)

#Rotas de Administrador
app.register_blueprint(admin_bp)

#Rotas para Usuário
app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run(debug=True)
