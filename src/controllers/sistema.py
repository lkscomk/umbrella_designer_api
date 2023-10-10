from flask import Blueprint, request
from src.database.bd import Database

sistema_bp = Blueprint('sistema', __name__)

@sistema_bp.route('/')
def informacoesSistema():
    return "Informações do Sistema"

@sistema_bp.route('/api/sistema/opcoes/<int:grupo>')
def opcoes(grupo=None):
    db = Database()
    if grupo is None:
        return { 'erro': 'Grupo obrigatório'}, 200
    else:
        params = "WHERE deleted_by is null"
        params += f" AND grupo = {grupo}" if grupo else ''
        resultado = db.selectAll('opcoes', params)

    db.__del__()
    return resultado
