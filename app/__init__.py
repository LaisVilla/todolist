from flask import Flask

# Função para criar a aplicação Flask
def create_app():
    # Instancia o objeto Flask que representa o aplicativo
    app = Flask(__name__)
    
    # Configura uma chave secreta para a aplicação
    # A chave secreta é usada para segurança, como a proteção de sessões e CSRF.
    app.config['SECRET_KEY'] = 'chave-secreta-do-app'
    
    # Importa e registra o Blueprint chamado "main"
    # O Blueprint organiza rotas e lógica relacionadas, facilitando a modularidade do código.
    from app.routes import main
    app.register_blueprint(main)
    
    # Retorna a aplicação configurada
    return app
