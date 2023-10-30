from flask import Blueprint, request
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio, verificar_maioridade
from src.middlewares.autenticacao import autenticacao
from src.helpers.gerador import obter_datatime

telas = Blueprint('telas', __name__)

# variaveiss
endPoint = '/api/telas'

@autenticacao
@telas.route(f"{endPoint}", methods=['GET'])
def listar():
    db = Database()

    nome = request.args.get('nome')

    params = "WHERE deleted_at is null"
    params += f" AND nome LIKE '%{nome}%'" if nome else ''

    resultado = db.selectAll('acesso_tela', params)

    db.__del__()
    return resultado

@autenticacao
@telas.route(f"{endPoint}-acessos/<int:telaId>", methods=['GET'])
def listarAcessos(telaId):
    db = Database()

    descricao = request.args.get('descricao')

    query = f"""
        SELECT acesso.id
             , opcoes.descricao
        	 , acesso.created_at
             , acesso.created_by
        FROM tipo_usuario_tem_acesso_tela as acesso

        INNER
        JOIN opcoes as opcoes
           ON opcoes.grupo = 2
          AND opcoes.item = acesso.tipo_usuario_id


        WHERE acesso.deleted_at is null
          AND acesso.acesso_tela_id = {telaId}"""
    query += f" AND opcoes.descricao LIKE '%{descricao}%'" if descricao else ''

    resultado = db.sql(query)

    db.__del__()
    return resultado


@autenticacao
@telas.route(f"{endPoint}/<int:id>", methods=['GET'])
def exibir(id):
    db = Database()

    resultado = db.selectOne('usuario', id)

    db.__del__()
    return resultado

@telas.route(f"{endPoint}", methods=['POST'])
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
@telas.route(f"{endPoint}/<int:id>", methods=['PUT'])
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
@telas.route(f"{endPoint}/<int:id>", methods=['DELETE'])
def excluir(id):
    db = Database()
    login = request.headers.get('Login')
    a = db.remove('usuario', login, id)
    db.__del__()
    return { 'mensagem': 'Usuário excluído com sucesso!'}
