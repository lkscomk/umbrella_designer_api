from flask import Blueprint, request, jsonify
import os
from src.database.bd import Database
from src.middlewares.autenticacao import autenticacao

portfolio = Blueprint('portfolio', __name__)

endPoint = '/api/portfolio'

#nesse aquivo deve ficar as rotas de
# listar
# exibir
# inserir
# editar
# deletar
