from flask import request
import flask
from flask_restful import Resource
import jwt
from datetime import datetime, timedelta
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio

# Configurando o tempo de expiração do token (1 hora)
expiration_time = datetime.utcnow() + timedelta(hours=1)

class Login(Resource):
  def post(self):
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