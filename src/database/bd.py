import os
import mysql.connector
from dotenv import load_dotenv
from src.helpers.validador import serializar_data
from src.helpers.gerador import obter_datatime
import json
import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.cur = None
        load_dotenv()
        self.ambiente = 'dev'
        if (self.ambiente == 'dev'):
            self.connect_dev()
        else:
            self.connect_producao()

    def connect_producao(self):
        banco = f'{os.path.dirname(os.path.abspath(__file__))}/banco.db'
        self.conn = sqlite3.connect(banco)
        self.cur = self.conn.cursor()

    def connect_dev(self):
        load_dotenv()  # Carregue as variáveis de ambiente do arquivo .env
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")

        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_database
            )
            self.cur = self.conn.cursor()
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def selectAll(self, tabela, params = None):
        try:
            if params is None:
                query = f"SELECT * FROM {tabela}"
            else:
                query = f"SELECT * FROM {tabela} {params}"

            print(query)

            self.cur.execute(query)
            rows = self.cur.fetchall()
            column_names = [desc[0] for desc in self.cur.description]

            resultados = []
            for row in rows:
                resultado_dict = {}
                for i, value in enumerate(row):
                    resultado_dict[column_names[i]] = value
                resultados.append(resultado_dict)

            json_string = json.dumps(resultados, default=serializar_data)

            return json.loads(json_string)
        except mysql.connector.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []

    def selectOne(self, tabela, id, params = None):
        try:
            query = f"SELECT * FROM {tabela} WHERE id = {id} AND deleted_by is null"

            print(query)

            self.cur.execute(query)
            row = self.cur.fetchone()
            resultado = {}

            if row is not None:
                nomes_colunas = [coluna[0] for coluna in self.cur.description]

                resultado = dict(zip(nomes_colunas, row))

            json_string = json.dumps(resultado, default=serializar_data)

            return json.loads(json_string)
        except mysql.connector.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return []

    def sql(self, query):
        try:
            print(query)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            column_names = [desc[0] for desc in self.cur.description]

            resultados = []
            for row in rows:
                resultado_dict = {}
                for i, value in enumerate(row):
                    resultado_dict[column_names[i]] = value
                resultados.append(resultado_dict)

            json_string = json.dumps(resultados, default=serializar_data)

            return json.loads(json_string)
        except mysql.connector.Error as e:
            print(f"Erro ao rodar código: {e}")
            return 0

    def insert(self, tabela, valores):
        try:
            query = f"""
            INSERT
              INTO {tabela} {str(tuple(valores.keys())).replace("'", '').replace('"', "")}
            VALUES {tuple(valores.values())};
            """
            print(query)
            self.cur.execute(query)
            self.conn.commit()
            return self.cur.lastrowid  # Retorna o ID do último registro inserido
        except mysql.connector.Error as e:
            print(f"Erro ao inserir os dados: {e}")
            return None

    def remove(self, tabela, usuarioExclusao, id):
        try:
            res = self.selectOne(tabela, id)

            if len(res) < 0:
                return { 'mensagem': 'Registro não encontrado!' }
            else:
              query = f"""
              UPDATE {tabela} SET deleted_by = '{usuarioExclusao}', `deleted_at` = '{obter_datatime()}' WHERE (id = {id});
              """

              print(query)
              self.cur.execute(query)
              self.conn.commit()
              return self.cur.lastrowid
        except mysql.connector.Error as e:
            print(f"Erro ao remover os dados: {e}")
            return 0

    def update(self, tabela, valores, id):
        try:
            params = ', '.join([f"{chave} = '{valor}'" for chave, valor in valores.items()])

            query = f"""
            UPDATE {tabela} SET {params}
            WHERE id = {id}
            """
            print(query)

            self.cur.execute(query)
            self.conn.commit()
            return self.cur.rowcount
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar os dados: {e}")
            return 0

    def obter_informacoes_tabelas(self):
        try:
            if (self.ambiente == 'dev'):
                # Obter nomes das tabelas
                self.cur.execute("SHOW TABLES;")
                tabelas = [tabela[0] for tabela in self.cur.fetchall()]

                # Crie um dicionário para armazenar as informações
                informacoes = {}
                for tabela in tabelas:
                    # Obter informações sobre colunas
                    self.cur.execute(f"DESCRIBE {tabela};")
                    colunas = [coluna[0] for coluna in self.cur.fetchall()]

                    # Obter quantidade de registros
                    self.cur.execute(f"SELECT COUNT(*) FROM {tabela};")
                    quantidade_registros = self.cur.fetchone()[0]

                    # Obter todos os registros
                    res = self.selectAll(tabela)

                    informacoes[tabela] = {
                        "colunas": colunas,
                        "quantidade_registros": quantidade_registros,
                        "registros": res
                    }

                return informacoes
            else:
                self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tabelas = self.cur.fetchall()
                tabelas = [tabela[0] for tabela in tabelas]

                # Crie um dicionário para armazenar as informações
                informacoes = {}
                for tabela in tabelas:
                    self.cur.execute(f"PRAGMA table_info({tabela});")
                    colunas = self.cur.fetchall()
                    coluna_nomes = [coluna[1] for coluna in colunas]

                    self.cur.execute(f"SELECT COUNT(*) FROM {tabela};")
                    quantidade_registros = self.cur.fetchone()[0]

                    res = self.selectAll(tabela)

                    informacoes[tabela] = {
                        "colunas": coluna_nomes,
                        "quantidade_registros": quantidade_registros,
                        "registros": res
                    }

                    return informacoes
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
