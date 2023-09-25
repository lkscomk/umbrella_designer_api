from flask import request
from flask_restful import Resource
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio


class Opcoes(Resource):
    def get(self, grupo=None):
        db = Database()
        descricao = request.args.get('descricao')

        if grupo is None:
            grupo = request.args.get('grupo')


        if grupo is None:
            return { 'erro': 'Grupo obrigatório'}, 200
        else:
            params = "WHERE deleted_by is null"
            params += f" AND grupo = {grupo}" if grupo else ''
            params += f" AND descricao LIKE '%{descricao}%'" if descricao else ''
            resultado = db.selectAll('opcoes', params)

        db.__del__()
        return resultado
    def post(self):
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
