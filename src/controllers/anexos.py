from flask import Blueprint, request, jsonify
from src.database.bd import Database
from dotenv import load_dotenv
import os
import requests
from src.helpers.validador import validar_obrigatorio
from src.helpers.gerador import gerador_checksum
from src.middlewares.autenticacao import autenticacao

anexos = Blueprint('anexos', __name__)

endPoint = '/api/anexos'

@autenticacao
@anexos.route(f"{endPoint}", methods=['GET'])
def listar():
    db = Database()

    params = "WHERE deleted_by is null"
    resultado = db.selectAll('anexos', params)

    db.__del__()
    return resultado, 200

@autenticacao
@anexos.route(f"{endPoint}/<int:id>", methods=['GET'])
def exibir(id):
    db = Database()

    resultado = db.selectOne('anexos', id)

    db.__del__()
    return resultado

@autenticacao
@anexos.route(f"{endPoint}", methods=['POST'])
def inserir():
    # pegar informacoes enviadas no body da requisição
    data = request.form

    # guarda as informacoes em variaveis
    file = request.files['file']
    nome_arquivo = '.'.join(file.filename.split('.')[0:-1])
    tipo = f".{file.filename.split('.')[-1]}"
    tabela = data['tabela']
    tabela_id = data['tabela_id']
    checksum = gerador_checksum()
    created_by = request.headers.get('Login')

    # validações
    obrigatorio = validar_obrigatorio(data, ['tabela', 'tabela_id'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo fornecido'}), 400

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    #envia arquivo para servidor de arquivo
    load_dotenv()
    servidor = os.getenv("SERVIDOR_ARQUIVOS")
    response = requests.request("POST", f"{servidor}/upload", data={
                            "checksum": checksum,
                            "tipo": tipo
                            }, files=request.files)
    tamanho = dict(response.json())['tamanho_bytes']


    # insere informacoes no banco
    db = Database()
    anexos = db.insert('anexos', {
                            "tabela": tabela,
                            "tabela_id": tabela_id,
                            "nome": nome_arquivo,
                            "checksum": checksum,
                            "tipo": tipo,
                            "tamanho": tamanho,
                            "created_by": created_by
                            })

    # finaliza conexao com banco
    db.__del__()

    # retorna mensagem de responsta
    return { 'id': anexos, 'mensagem': 'Usuário cadastrado com sucesso'}, 200

@autenticacao
@anexos.route(f"{endPoint}/<int:id>", methods=['PUT'])
def editar(id):
    db = Database()
    data = request.get_json()
    login = request.headers.get('Login')

    nome = data.get('nome')
    data_nascimento = data.get('data_nascimento')
    cpf = data.get('cpf')
    tipo = data.get('tipo')

    params = { 'nome': nome.upper(), 'data_nascimento': data_nascimento, 'cpf': cpf, 'tipo_anexo_id': tipo, 'updated_by': login, 'updated_at': obter_datatime()}

    if id is None:
        return { "erro": "Id do usuário é Obrigatorio!" }, 500

    if login is None:
        return { "erro": "Login do usuário é Obrigatorio!" }, 500

    maioridade = verificar_maioridade(data_nascimento)
    if maioridade is not True:
        return { "erro": maioridade }, 500

    resultado = db.selectOne('anexos', id)
    if not resultado:
        return {"erro": 'Usuário não encontrado.'}

    res = db.update('anexos', params, id)
    db.__del__()
    return { 'id': id, 'mensagem': 'Usuário atualizado com sucesso' }

@autenticacao
@anexos.route(f"{endPoint}/<int:id>", methods=['DELETE'])
def excluir(id):
    db = Database()
    login = request.headers.get('Login')
    a = db.remove('anexos', login, id)
    db.__del__()
    return { 'mensagem': 'Usuário excluído com sucesso!'}


