from flask import Blueprint, request
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio, verificar_maioridade
from src.middlewares.autenticacao import autenticacao
from src.helpers.gerador import obter_datatime

usuario = Blueprint('usuario', __name__)

# variaveis
endPoint = '/api/usuario'

@autenticacao
@usuario.route(f"{endPoint}", methods=['GET'])
def listar():
    db = Database()

    tipos = request.args.getlist('tipo[]')
    id = request.args.get('id')
    nome = request.args.get('nome')
    email = request.args.get('email')
    cpf = request.args.get('cpf')

    params = """
    SELECT usuario.id
            , usuario.tipo_usuario_id
            , opcoes.descricao as tipo
            , usuario.data_nascimento
            , usuario.nome
            , usuario.email
            , usuario.cpf
            , usuario.created_at
        FROM umbrella.usuario
    INNER
        JOIN umbrella.opcoes as opcoes
        ON opcoes.deleted_by is null
        AND opcoes.grupo = 2 -- TIPOS DE USUARIOS
        AND opcoes.item = usuario.tipo_usuario_id
    WHERE usuario.deleted_by is null
    """

    params += f" AND usuario.id in ({id})" if id else ''
    params += f" AND usuario.tipo_usuario_id in ({', '.join(tipos)})" if tipos else ''
    params += f" AND usuario.nome LIKE '%{nome}%'" if nome else ''
    params += f" AND usuario.email LIKE '%{email}%'" if email else ''
    params += f" AND usuario.cpf LIKE '%{cpf}%'" if cpf else ''

    resultado = db.sql(params)

    db.__del__()
    return resultado

@autenticacao
@usuario.route(f"{endPoint}/<int:id>", methods=['GET'])
def exibir(id):
    db = Database()

    resultado = db.selectOne('usuario', id)

    db.__del__()
    return resultado

@usuario.route(f"{endPoint}", methods=['POST'])
def inserir():
    # pegar informacoes enviadas no body da requisição
    data = request.get_json()

    # guarda as informacoes em variaveis
    tipoUsuarioId = data.get('tipoUsuarioId')
    dataNascimento = data.get('dataNascimento')
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    cpf = data.get('cpf')
    email_status_id = 2 #email nao verificado

    obrigatorio = validar_obrigatorio(data, ['tipoUsuarioId', 'dataNascimento', 'nome', 'email', 'senha', 'cpf'])
    if obrigatorio is not True:
        return { "erro": obrigatorio }, 500

    maioridade = verificar_maioridade(dataNascimento)
    if maioridade is not True:
        return { "erro": maioridade }, 500

    # inicia conexao com banco de dados
    db = Database()

    #verificar se email ja esta cadastrado existe
    params = "WHERE deleted_by is null"
    params += f" AND email = '{email}'" if email else ''

    resultado = db.selectAll('usuario', params)
    if len(resultado) != 0:
        return {"erro": "Já existe um usuário cadastrato com este email."}, 200


    # insere informacoes no banco
    usuario = db.insert('usuario', {
                            "tipo_usuario_id": tipoUsuarioId,
                            "data_nascimento": dataNascimento,
                            "nome": nome.upper(),
                            "email": email,
                            "email_status_id": email_status_id,
                            "senha": senha,
                            "cpf": cpf,
                            "created_by": "API"
                            })

    # finaliza conexao com banco
    db.__del__()

    # retorna mensagem de responsta
    return { 'id': usuario, 'mensagem': 'Usuário cadastrado com sucesso'}, 200

@autenticacao
@usuario.route(f"{endPoint}/<int:id>", methods=['PUT'])
def editar(id):
    db = Database()
    data = request.get_json()
    login = request.headers.get('Login')

    nome = data.get('nome')
    data_nascimento = data.get('data_nascimento')
    cpf = data.get('cpf')
    tipo = data.get('tipo')

    params = { 'nome': nome.upper(), 'data_nascimento': data_nascimento, 'cpf': cpf, 'tipo_usuario_id': tipo, 'updated_by': login, 'updated_at': obter_datatime()}

    if id is None:
        return { "erro": "Id do usuário é Obrigatorio!" }, 500

    if login is None:
        return { "erro": "Login do usuário é Obrigatorio!" }, 500

    maioridade = verificar_maioridade(data_nascimento)
    if maioridade is not True:
        return { "erro": maioridade }, 500

    resultado = db.selectOne('usuario', id)
    if not resultado:
        return {"erro": 'Usuário não encontrado.'}

    res = db.update('usuario', params, id)
    db.__del__()
    return { 'id': id, 'mensagem': 'Usuário atualizado com sucesso' }

@autenticacao
@usuario.route(f"{endPoint}/<int:id>", methods=['DELETE'])
def excluir(id):
    db = Database()
    login = request.headers.get('Login')
    a = db.remove('usuario', login, id)
    db.__del__()
    return { 'mensagem': 'Usuário excluído com sucesso!'}
