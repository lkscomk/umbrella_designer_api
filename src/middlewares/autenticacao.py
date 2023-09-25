from functools import wraps
from flask import request
from datetime import datetime
import jwt

def autenticacao(f):
  @wraps(f)
  def decorated_function(*args, **kws):
    token = str(request.headers.get('Authorization')).replace('Bearer ', '')
    if token == 'None':
      return { "mensagem": "Token de acesso não informado!" }
    try:
      # Decodificando o token
      payload = jwt.decode(token, 'teste', algorithms=['HS256'])
      # Verificando se o token não expirou
      if datetime.now() > datetime.fromtimestamp(payload['exp']):
        raise Exception('Token expirado')

    except Exception as e:
        return { 'mensagem': f'Usuário não autenticado. {e}' }, 401
    return f(*args, **kws)
  return decorated_function



