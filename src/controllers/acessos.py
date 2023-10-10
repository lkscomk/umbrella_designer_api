from flask import request
from flask_restful import Resource
from src.database.bd import Database
from src.middlewares.autenticacao import autenticacao


class Acessos(Resource):
    @autenticacao
    def get(self, id=None):
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
