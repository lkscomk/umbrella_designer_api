from flask import Blueprint, request
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio
from src.middlewares.autenticacao import autenticacao
from src.helpers.gerador import obter_datatime

opcoes = Blueprint('opcoes', __name__)

endPoint = '/api/opcoes'

@opcoes.route(f"{endPoint}", methods=['GET'])
@autenticacao
def listar(id=None):
    db = Database()
    descricao = request.args.get('descricao')
    grupo = request.args.get('grupo')

    sql = f"""
        SELECT opcoes.id
                , opcoes.grupo
                , opcoes2.descricao AS descricaoGrupo
                , opcoes.item
                , opcoes.descricao
                , opcoes.created_by
                , opcoes.created_at
            FROM umbrella.opcoes AS opcoes
        INNER
            JOIN umbrella.opcoes AS opcoes2
            ON opcoes2.deleted_at IS null
            AND opcoes2.grupo = 1
            AND opcoes2.item = opcoes.grupo
        WHERE opcoes.deleted_by is null
    """

    if id is None:
        sql += f" AND opcoes.grupo = {grupo}" if grupo else ''
        sql += f" AND opcoes.descricao LIKE '%{descricao}%'" if descricao else ''
        sql += " ORDER BY opcoes.item;"
        resultado = db.sql(sql)
    else:
        resultado = db.selectOne('opcoes', id)

    db.__del__()
    return resultado

@opcoes.route(f"{endPoint}/<int:id>", methods=['GET'])
def exibir(id):
    db = Database()
    resultado = db.selectOne('opcoes', id)

    db.__del__()
    return resultado

@opcoes.route(f"{endPoint}/", methods=['POST'])
@autenticacao
def inserir():
    # pegar informacoes enviadas no body da requisição
    data = request.get_json()

    # guarda as informacoes em variaveis
    grupo = data.get('grupo')
    item = data.get('item')
    descricao = data.get('descricao')
    created_by = request.headers.get('login')

    obrigatorio = validar_obrigatorio(data, ['grupo', 'item', 'descricao'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    # inicia conexao com banco de dados
    db = Database()

    #verificar se email ja esta cadastrado existe
    params = "WHERE deleted_by is null"
    params += f" AND grupo = '{grupo}'" if grupo else ''
    params += f" AND item = '{item}'" if item else ''

    resultado = db.selectAll('opcoes', params)
    if len(resultado) != 0:
        return {"erro": "Já existe um grupo/item informado."}, 200


    # insere informacoes no banco
    usuario = db.insert('opcoes', {
                            "grupo": grupo,
                            "item": item,
                            "descricao": descricao.upper(),
                            "created_by": created_by
                            })

    # finaliza conexao com banco
    db.__del__()

    # retorna mensagem de responsta
    return { 'id': usuario, 'mensagem': 'Usuário cadastrado com sucesso'}, 200

@opcoes.route(f"{endPoint}/<int:id>", methods=['PUT'])
@autenticacao
def editar(id):
    db = Database()
    data = request.get_json()
    login = request.headers.get('Login')
    descricao = data.get('descricao')

    params = { 'descricao': descricao.upper(), 'updated_by': login, 'updated_at': obter_datatime()}

    obrigatorio = validar_obrigatorio(data, ['descricao'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    # inicia conexao com banco de dados
    db = Database()

    resultado = db.selectOne('opcoes', id)
    if not resultado:
        return {"erro": 'Registro não encontrado.'}


    res = db.update('opcoes', params, id)
    db.__del__()
    return { 'id': res, 'mensagem': 'Registro atualizado com sucesso'}

@opcoes.route(f"{endPoint}/<int:grupo>", methods=['DELETE'])
@autenticacao
def excluir(id=None):
        db = Database()
        login = request.headers.get('Login')
        a = db.remove('opcoes', login, id)
        db.__del__()
        return { 'id': id, 'mensagem': 'Registro excluído com sucesso!'}