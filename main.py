from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.controllers.usuarios import Usuario
from src.controllers.opcoes import Opcoes
from src.controllers.login import Login
from src.controllers.acessos import Acessos
from src.controllers.sistema import sistema_bp

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

    api = Api(app)

    api.add_resource(Login, '/api/login')
    api.add_resource(Opcoes, '/api/opcoes/<int:id>', '/api/opcoes')
    api.add_resource(Usuario, '/api/usuario/<int:id>', '/api/usuario')
    api.add_resource(Acessos, '/api/acessos_tela/<int:id>')

    app.register_blueprint(sistema_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
