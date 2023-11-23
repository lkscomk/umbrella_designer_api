from flask import Blueprint, request,jsonify
from src.database.bd import Database
import jwt
import requests
from datetime import datetime, timedelta
from src.helpers.validador import validar_obrigatorio
from src.middlewares.autenticacao import autenticacao

sistema = Blueprint('sistema', __name__)

# variaveis
endPoint = '/api/sistema/'
expiration_time = datetime.utcnow() + timedelta(hours=1)


@sistema.route(f"{endPoint}", methods=['GET'])
def statusSistema():
    return "Informações do Sistema"

@sistema.route(f"{endPoint}/login", methods=['POST'])
def login():
    try:
      data = request.get_json()

      resultado = validar_obrigatorio(data, ['email', 'senha'])
      if resultado is not True:
          return resultado, 500

      email = data.get("email")
      senha = data.get("senha")

      params = "WHERE deleted_by is null"
      params += f" AND upper(email) = upper('{email}')" if email else ''
      params += f" AND senha = '{senha}'" if senha else ''

      db = Database()
      resultado = db.selectAll('usuario', params)

      if len(resultado) == 0:
        return {"erro": "Usuário não encontrado ou senha incorreta."}, 200

      usuario = resultado[0]

      payload = {'email': email, 'exp': expiration_time}

      # Gerando o token
      token = jwt.encode(payload, 'teste', algorithm='HS256')
      return { "mensagem": "Usuário logado com sucesso!",
               "email": email,
               "nome": usuario["nome"],
               "login": f"{usuario['id']}-{usuario['nome'].split(' ')[0]}",
               "id": usuario['id'],
               "token": token
             }, 200
    except Exception as e:
            return {"erro": f"Erro ao processar a solicitação: {str(e)}"}, 500

@autenticacao
@sistema.route(f"{endPoint}/acessos_tela/<int:id>", methods=['GET'])
def listarAcessos(id=None):
    db = Database()

    if id is None:
        return {"erro": 'Id do usuário não informado.'}

    resultado = db.selectOne('usuario', id)
    if not resultado:
        return {"erro": 'Usuário não encontrado.'}


    sql = f"""
        SELECT usuario.nome
                , usuario.tipo_usuario_id
                , acesso.nome
                , acesso.url
            FROM umbrella.usuario as usuario

            INNER
            JOIN umbrella.opcoes as opcoes
            ON opcoes.deleted_at is null
            AND opcoes.grupo = 2
            AND opcoes.item = usuario.tipo_usuario_id

            INNER
            JOIN umbrella.tipo_usuario_tem_acesso_tela as acesso_tela
            ON acesso_tela.deleted_at is null
            AND usuario.tipo_usuario_id = acesso_tela.tipo_usuario_id

            INNER
            JOIN umbrella.acesso_tela as acesso
            ON usuario.deleted_at is null
            AND acesso.id = acesso_tela.acesso_tela_id

            WHERE usuario.deleted_at is null
            AND usuario.id = {id}
    """

    res = db.sql(sql)

    db.__del__()
    return res


@sistema.route(f"{endPoint}/opcoes/<int:grupo>", methods=['GET'])
def listarDropdown(grupo=None):
    db = Database()
    if grupo is None:
        return { 'erro': 'Grupo obrigatório'}, 200
    else:
        params = "WHERE deleted_by is null"
        params += f" AND grupo = {grupo}" if grupo else ''
        resultado = db.selectAll('opcoes', params)

    db.__del__()
    return resultado

@sistema.route('/informacoes_tabelas', methods=['GET'])
def obter_informacoes_tabelas():
  try:
    db = Database()

    # Obtenha uma lista de todas as tabelas no banco de dados
    res = db.obter_informacoes_tabelas()
    db.__del__()
    return jsonify(res)

  except Exception as e:
    return jsonify({"error": str(e)})

@sistema.route('/backup_producao', methods=['GET'])
def obter_backup_producao():
    import requests

    url = "https://umbrella.lukasrocha.repl.co/informacoes_tabelas"

    response = requests.request("GET", url)

    return 'response'