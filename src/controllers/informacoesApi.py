from flask import jsonify
from flask_restful import Resource


class InformacoesAPI(Resource):

  def get(self):
    autor = "Seu nome aqui"
    descricao = "API para enviar emails"

    return jsonify(autor=autor, descricao=descricao)
