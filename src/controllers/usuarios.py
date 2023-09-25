from flask import request
from flask_restful import Resource
from src.database.bd import Database
from src.helpers.validador import validar_obrigatorio, verificar_maioridade
from src.middlewares.autenticacao import autenticacao


class Usuario(Resource):
    @autenticacao
    def get(self, id=None):
        db = Database()

        if id is None:
            tipoUsuarioId = request.args.get('tipoUsuarioId[]')
            dataNascimento = request.args.get('dataNascimento')
            nome = request.args.get('nome')
            email = request.args.get('email')
            cpf = request.args.get('cpf')

            params = "WHERE deleted_by is null"
            params += f" AND tipo_usuario_id in {tipoUsuarioId}" if tipoUsuarioId else ''
            params += f" AND data_nascimento = '{dataNascimento}'" if dataNascimento else ''
            params += f" AND nome LIKE '%{nome}%'" if nome else ''
            params += f" AND email  LIKE '%{email}%'" if email else ''
            params += f" AND cpf = '{cpf}'" if cpf else ''

            resultado = db.selectAll('usuario', params)
        else:
            resultado = db.selectOne('usuario', id)

        db.__del__()
        return resultado

    def post(self):
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
                              "created_by": "1-LUKAS"
                              })

        # finaliza conexao com banco
        db.__del__()

        # retorna mensagem de responsta
        return { 'id': usuario, 'mensagem': 'Usuário cadastrado com sucesso'}, 200

    def put(self, id):
        data = request.get_json()
        titulo = data.get('titulo')
        autor = data.get('autor')
        ano = data.get('ano')
        db = Database()
        query = "UPDATE livros SET título = ?, autor = ?, ano = ? WHERE id = ?"
        params = (titulo, autor, ano, id)
        db.update(query, params)
        db.__del__()
        return {'mensagem': 'Livro atualizado com sucesso'}

    def delete(self, id):
        db = Database()
        query = "DELETE FROM livros WHERE id = ?"
        params = (id,)
        db.remove(query, params)
        db.__del__()
        return {'mensagem': 'Livro removido com sucesso'}
