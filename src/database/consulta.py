import sqlite3

# Conecte-se ao banco de dados SQLite (substitua 'seu_banco_de_dados.db' pelo nome do seu arquivo de banco de dados)
conn = sqlite3.connect('banco.db')

# Crie um cursor
cursor = conn.cursor()

# Execute uma consulta SQL para selecionar todas as informações da tabela 'usuario'
cursor.execute('SELECT * FROM acesso_tela')

# Recupere todas as linhas da consulta
rows = cursor.fetchall()

# Exiba as informações recuperadas
for row in rows:
    print(row)

# Execute uma consulta SQL para selecionar todas as informações da tabela 'usuario'
cursor.execute('SELECT * FROM usuario')

# Recupere todas as linhas da consulta
rows = cursor.fetchall()

# Exiba as informações recuperadas
for row in rows:
    print(row)

# Execute uma consulta SQL para selecionar todas as informações da tabela 'usuario'
cursor.execute('SELECT * FROM anexos')

# Recupere todas as linhas da consulta
rows = cursor.fetchall()

# Exiba as informações recuperadas
for row in rows:
    print(row)

# Feche a conexão com o banco de dados
conn.close()
