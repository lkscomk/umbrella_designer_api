from flask import request
from flask_restful import Resource
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio
from src.helpers.gerador import gerador_codigo_seguranca



class EnviarEmail(Resource):
    def post(self):
        # pegar informacoes enviadas no body da requisição
        data = request.get_json()

        # guarda as informacoes em variaveis
        titulo = data.get('titulo')
        mensagem = data.get('mensagem')
        email_envio = data.get('email_envio')
        tipo_email_id = data.get('tipo_email_id')
        para_usuario_id = data.get('para_usuario_id')

        obrigatorio = validar_obrigatorio(data, ['titulo', 'mensagem', 'email_envio', 'tipo_email_id', 'para_usuario_id'])
        if obrigatorio is not True:
            return { "erro": obrigatorio }, 500

        # inicia conexao com banco de dados
        db = Database()


        # insere informacoes no banco
        usuario = db.insert('fila_email', {
                            "titulo": titulo,
                            "mensagem": mensagem,
                            "email_envio": email_envio,
                            "tipo_email_id": tipo_email_id,
                            "para_usuario_id": para_usuario_id,
                            "created_by": "API"
                            })

        # finaliza conexao com banco
        db.__del__()

        codigo_seguranca = gerador_codigo_seguranca()

        # retorna mensagem de responsta
        return { 'mensagem': 'Usuário cadastrado com sucesso', 'valor': codigo_seguranca }, 200
