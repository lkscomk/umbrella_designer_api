from flask import Blueprint, request, jsonify
import os
from src.database.bd import Database
from src.middlewares.autenticacao import autenticacao

pedido = Blueprint('pedido', __name__)

endPoint = '/api/pedido'

#nesse aquivo deve ficar as rotas de
# listar
# exibir
# inserir
# editar
# deletar

# aceitar
# enviar pedido
# pedir alteração

# tudo envolvendo os pedidos tanto as rotas que envolvem o cliente quando as que envolvem o prestador


