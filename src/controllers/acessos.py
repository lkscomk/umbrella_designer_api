from flask import Blueprint, request
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio
from src.middlewares.autenticacao import autenticacao
from src.helpers.gerador import obter_datatime

acessos = Blueprint('acessos', __name__)

endPoint = '/api/acessos'

@acessos.route(f"{endPoint}", methods=['GET'])
# @autenticacao
def listar(id=None):
    nome = request.args.get('nome')
    codigo = request.args.get('codigo')

    db = Database()
    if id is None:
        params = "WHERE deleted_by is null"
        params += f" AND acesso_tela.id in ({codigo})" if codigo else ''
        params += f" AND acesso_tela.nome LIKE '%{nome}%'" if nome else ''
        resultado = db.selectAll('acesso_tela', params)
    else:
        resultado = db.selectOne('acessos', id)

    db.__del__()
    return resultado

@acessos.route(f"{endPoint}/<int:id>", methods=['GET'])
# @autenticacao
def exibir(id):
    db = Database()
    resultado = db.selectOne('acesso_tela', id)

    db.__del__()
    return resultado

@acessos.route(f"{endPoint}/", methods=['POST'])
# @autenticacao
def inserir():
    # pegar informacoes enviadas no body da requisição
    data = request.get_json()

    # guarda as informacoes em variaveis
    nome = data.get('nome')
    url = data.get('url')
    created_by = request.headers.get('login')

    obrigatorio = validar_obrigatorio(data, ['nome', 'url'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    # inicia conexao com banco de dados
    db = Database()

    # insere informacoes no banco
    usuario = db.insert('acesso_tela', {
                            "nome": nome.upper(),
                            "url": url,
                            "created_by": created_by
                            })

    # finaliza conexao com banco
    db.__del__()

    # retorna mensagem de responsta
    return { 'id': usuario, 'mensagem': 'Tela cadastrada com sucesso'}, 200

@acessos.route(f"{endPoint}/<int:id>", methods=['PUT'])
# @autenticacao
def editar(id):
    db = Database()
    data = request.get_json()
    login = request.headers.get('Login')
    nome = data.get('nome')
    url = data.get('url')

    params = { 'nome': nome.upper(), 'url': url, 'updated_by': login, 'updated_at': obter_datatime()}

    obrigatorio = validar_obrigatorio(data, ['nome', 'url'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    # inicia conexao com banco de dados
    db = Database()

    resultado = db.selectOne('acesso_tela', id)
    if not resultado:
        return {"erro": 'Registro não encontrado.'}


    res = db.update('acesso_tela', params, id)
    db.__del__()
    return { 'id': res, 'mensagem': 'Registro atualizado com sucesso'}

@acessos.route(f"{endPoint}/<int:id>", methods=['DELETE'])
# @autenticacao
def excluir(id=None):
        db = Database()
        login = request.headers.get('Login')
        a = db.remove('acesso_tela', login, id)
        db.__del__()
        return { 'id': id, 'mensagem': 'Registro excluído com sucesso!'}

@acessos.route(f"{endPoint}-tipo", methods=['GET'])
# @autenticacao
def listar_acessos(id=None):
    descricao = request.args.get('descricao')
    tela = request.args.get('tela')
    params = """
     SELECT acesso.id
          , tela.nome
          , opcoes.item
          , opcoes.descricao
          , acesso.created_at
          , acesso.created_by

       FROM umbrella.tipo_usuario_tem_acesso_tela as acesso

      INNER
       JOIN acesso_tela as tela
         ON tela.id = acesso.acesso_tela_id

      INNER
       JOIN opcoes
         ON opcoes.grupo =  2 -- tipos de usuario
        AND opcoes.item = acesso.tipo_usuario_id

      WHERE tela.deleted_at is null
    """
    db = Database()
    params += f" AND tela.id in ({tela})" if tela else ''
    params += f" AND opcoes.descricao LIKE '%{descricao}%'" if descricao else ''
    resultado = db.sql(params)

    db.__del__()
    return resultado

@acessos.route(f"{endPoint}-tipo", methods=['POST'])
# @autenticacao
def inserir_acessos():
    # pegar informacoes enviadas no body da requisição
    data = request.get_json()

    # guarda as informacoes em variaveis
    tela = data.get('tela')
    tipo = data.get('tipo')
    created_by = request.headers.get('login')

    obrigatorio = validar_obrigatorio(data, ['tela', 'tipo'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    # inicia conexao com banco de dados
    db = Database()

    #verificar se ja esta cadastrado
    params = "WHERE deleted_by is null"
    params += f" AND acesso_tela_id = '{tela}'" if tela else ''
    params += f" AND tipo_usuario_id = '{tipo}'" if tipo else ''

    resultado = db.selectAll('tipo_usuario_tem_acesso_tela', params)
    if len(resultado) != 0:
        return {"erro": "Já existe um acesso para este tipo de usuário."}, 200

    # insere informacoes no banco
    usuario = db.insert('tipo_usuario_tem_acesso_tela', {
                            "acesso_tela_id": tela,
                            "tipo_usuario_id": tipo,
                            "created_by": created_by
                            })

    # finaliza conexao com banco
    db.__del__()

    # retorna mensagem de responsta
    return { 'id': usuario, 'mensagem': 'Tela cadastrada com sucesso'}, 200

@acessos.route(f"{endPoint}-tipo/<int:id>", methods=['DELETE'])
# @autenticacao
def excluir(id=None):
        db = Database()
        login = request.headers.get('Login')
        a = db.remove('tipo_usuario_tem_acesso_tela', login, id)
        db.__del__()
        return { 'id': id, 'mensagem': 'Registro excluído com sucesso!'}
