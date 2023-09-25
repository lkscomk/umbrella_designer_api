import sqlite3
import os

# Nome do arquivo de banco de dados SQLite
banco = arquivo = f'{os.path.dirname(os.path.abspath(__file__))}/banco.db'

# Função para criar as tabelas
def criar_tabelas():
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()

    sql = """
DROP TABLE IF EXISTS acesso_tela;
CREATE TABLE acesso_tela (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  url TEXT NOT NULL,
  created_by TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  update_at TIMESTAMP DEFAULT NULL,
  dateled_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);

DROP TABLE IF EXISTS anexos;
CREATE TABLE anexos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tabela TEXT NOT NULL,
  tabela_id INTEGER NOT NULL,
  nome TEXT NOT NULL,
  checksum TEXT NOT NULL,
  tipo TEXT NOT NULL,
  tamanho INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);

DROP TABLE IF EXISTS cobranca;
CREATE TABLE cobranca (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  status_cobranca_id INTEGER NOT NULL,
  forma_pagamento_id INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  valor NUMERIC(16,2) NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (forma_pagamento_id) REFERENCES opcoes(id),
  FOREIGN KEY (status_cobranca_id) REFERENCES opcoes(id),
  FOREIGN KEY (pedido_id) REFERENCES pedido(id)
);

DROP TABLE IF EXISTS cores;
CREATE TABLE cores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  codigo_hexadecimal TEXT NOT NULL,
  ordem INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (pedido_id) REFERENCES pedido(id)
);

DROP TABLE IF EXISTS fila_email;
CREATE TABLE fila_email (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  mensagem TEXT NOT NULL,
  email_envio TEXT NOT NULL,
  para_usuario_id INTEGER DEFAULT NULL,
  tipo_email_id INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (tipo_email_id) REFERENCES opcoes(id),
  FOREIGN KEY (id) REFERENCES usuario(id)
);

DROP TABLE IF EXISTS opcoes;
CREATE TABLE opcoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grupo INTEGER NOT NULL,
  item INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);

INSERT INTO opcoes (id, grupo, item, descricao, created_by, created_at)
VALUES
  (1, 1, 1, 'GRUPO DE OPÇÕES', '1-LUKAS', '2023-09-16 00:45:55'),
  (2, 1, 2, 'TIPOS DE USUÁRIO', '1-LUKAS', '2023-09-16 00:45:55'),
  (3, 2, 1, 'ADMINISTRADOR', '1-LUKAS', '2023-09-16 00:45:55'),
  (4, 2, 2, 'CLIENTE', '1-LUKAS', '2023-09-16 00:45:55'),
  (5, 2, 3, 'PRESTADOR DE SERVIÇO', '1-LUKAS', '2023-09-16 00:45:55'),
  (6, 1, 3, 'TIPOS DE EMAIL', '1-LUKAS', '2023-09-19 21:07:56'),
  (7, 3, 1, 'CRIAR CONTA', '1-LUKAS', '2023-09-19 21:08:12'),
  (8, 1, 4, 'STATUS EMAIL USUÁRIO', '1-LUKAS', '2023-09-19 21:40:19'),
  (9, 4, 1, 'VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42'),
  (10, 4, 2, 'NÃO VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42'),
  (11, 2, 4, 'TESTE 1', '1-LUKAS', '2023-09-23 15:26:46'),
  (12, 2, 5, 'TESTE 1', '4-MARINA', '2023-09-23 15:27:11'),
  (13, 2, 6, 'TESTE 1', '4-MARINA', '2023-09-23 15:28:01'),
  (14, 2, 7, 'TESTE 1', '4-MARINA', '2023-09-23 15:28:27'),
  (15, 2, 8, 'TESTE DE SCO', '1-LUKAS', '2023-09-23 15:36:32'),
  (16, 2, 9, 'TESTSEFDS', '1-LUKAS', '2023-09-23 15:38:08'),
  (17, 2, 10, 'EITA ', '1-LUKAS', '2023-09-23 15:38:59');

DROP TABLE IF EXISTS pedido;
CREATE TABLE pedido (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_pedido_id INTEGER NOT NULL,
  autor_usuario_id INTEGER NOT NULL,
  prestador_usuario_id INTEGER NOT NULL,
  status_pedido_id INTEGER NOT NULL,
  titulo TEXT NOT NULL,
  subtituto TEXT NOT NULL,
  outros_detalhes TEXT DEFAULT NULL,
  redes_sociais_referencia TEXT DEFAULT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (status_pedido_id) REFERENCES opcoes(id),
  FOREIGN KEY (tipo_pedido_id) REFERENCES opcoes(id),
  FOREIGN KEY (autor_usuario_id) REFERENCES usuario(id),
  FOREIGN KEY (prestador_usuario_id) REFERENCES usuario(id)
);

DROP TABLE IF EXISTS tipo_usuario_tem_acesso_tela;
CREATE TABLE tipo_usuario_tem_acesso_tela (
  acesso_tela_id INTEGER NOT NULL,
  tipo_usuario_id INTEGER NOT NULL,
  PRIMARY KEY (acesso_tela_id, tipo_usuario_id),
  FOREIGN KEY (acesso_tela_id) REFERENCES acesso_tela(id),
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes(id)
);

DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_usuario_id INTEGER NOT NULL,
  data_nascimento DATE NOT NULL,
  nome TEXT NOT NULL,
  email TEXT NOT NULL,
  email_status_id INTEGER NOT NULL,
  senha TEXT NOT NULL,
  cpf TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes(id)
);
"""
    cursor.executescript(sql)

    # Confirmar as alterações e fechar a conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
