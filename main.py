from flask import Flask
from flask_cors import CORS
from src.controllers.usuarios import usuario
from src.controllers.sistema import sistema
from src.controllers.pedido import pedido
from src.controllers.opcoes import opcoes
from src.controllers.anexos import anexos
from src.controllers.portfolio import portfolio

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

    app.register_blueprint(usuario)
    app.register_blueprint(anexos)
    app.register_blueprint(sistema)
    app.register_blueprint(portfolio)
    app.register_blueprint(pedido)
    app.register_blueprint(opcoes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
