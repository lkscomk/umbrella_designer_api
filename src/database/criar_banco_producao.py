import sqlite3
import os

# Nome do arquivo de banco de dados SQLite
banco = arquivo = f'{os.path.dirname(os.path.abspath(__file__))}/banco.db'

# Função para criar as tabelas
def criar_tabelas():
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()

    sql = """
-- Tabela acesso_tela
CREATE TABLE IF NOT EXISTS acesso_tela (
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

-- Inserir dados na tabela acesso_tela
INSERT INTO acesso_tela (nome, url, created_by, created_at)
VALUES
  ('Informações Perfil', '/perfil', '1-LUKAS', '2023-09-26 21:08:32'),
  ('Opções', '/opcoes', '1-LUKAS', '2023-09-26 21:08:56'),
  ('Usuários', '/usuarios', '1-LUKAS', '2023-09-26 21:51:05'),
  ('Portfolio', '/portfolio', '1-LUKAS', '2023-09-26 21:51:05'),
  ('Meus Pedidos', '/meus-pedidos', '1-LUKAS', '2023-09-26 21:51:05'),
  ('Pedido', '/pedido', '1-LUKAS', '2023-09-26 21:51:05'),
  ('Ajuda', '/ajuda', '1-LUKAS', '2023-10-03 19:33:56'),
  ('Acessos', '/acessos', '1-LUKAS', '2023-10-04 14:55:23');

-- Tabela anexos
CREATE TABLE IF NOT EXISTS anexos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tabela TEXT NOT NULL,
  tabela_id INTEGER NOT NULL,
  nome TEXT NOT NULL,
  checksum TEXT NOT NULL,
  tipo TEXT NOT NULL,
  tamanho INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);

-- Tabela cobranca
CREATE TABLE IF NOT EXISTS cobranca (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  status_cobranca_id INTEGER NOT NULL,
  forma_pagamento_id INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  valor DECIMAL(16, 2) NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (forma_pagamento_id) REFERENCES opcoes (id),
  FOREIGN KEY (status_cobranca_id) REFERENCES opcoes (id),
  FOREIGN KEY (pedido_id) REFERENCES pedido (id)
);

-- Tabela cores
CREATE TABLE IF NOT EXISTS cores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  codigo_hexadecimal TEXT NOT NULL,
  ordem INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (pedido_id) REFERENCES pedido (id)
);

-- Tabela fila_email
CREATE TABLE IF NOT EXISTS fila_email (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  mensagem TEXT NOT NULL,
  email_envio TEXT NOT NULL,
  para_usuario_id INTEGER DEFAULT NULL,
  tipo_email_id INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (tipo_email_id) REFERENCES opcoes (id),
  FOREIGN KEY (para_usuario_id) REFERENCES usuario (id)
);

-- Tabela opcoes
CREATE TABLE IF NOT EXISTS opcoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grupo INTEGER NOT NULL,
  item INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);

-- Inserir dados na tabela opcoes
INSERT INTO opcoes (grupo, item, descricao, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 1, 'GRUPO DE OPÇÕES', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL),
  (1, 2, 'TIPOS DE USUÁRIO', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL),
  (2, 1, 'ADMINISTRADOR', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL),
  (2, 2, 'CLIENTE', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL),
  (2, 3, 'PRESTADOR DE SERVIÇO', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL),
  (1, 3, 'TIPOS DE EMAIL', '1-LUKAS', '2023-09-19 21:07:56', NULL, NULL),
  (3, 1, 'CRIAR CONTA', '1-LUKAS', '2023-09-19 21:08:12', NULL, NULL),
  (1, 4, 'STATUS EMAIL USUÁRIOS', '1-LUKAS', '2023-09-19 21:40:19', '1-LUKAS', '2023-10-04 21:51:13', NULL, NULL),
  (4, 1, 'VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42', NULL, NULL),
  (4, 2, 'NÃO VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42', NULL, NULL),
  (2, 4, 'TESTE 1', '1-LUKAS', '2023-09-23 15:26:46', NULL, NULL),
  (2, 5, 'TESTE 1', '4-MARINA', '2023-09-23 15:27:11', NULL, NULL),
  (2, 6, 'TESTE 1', '4-MARINA', '2023-09-23 15:28:01', NULL, NULL),
  (2, 7, 'TESTE 1', '4-MARINA', '2023-09-23 15:28:27', NULL, NULL),
  (2, 8, 'TESTE DE SCO', '1-LUKAS', '2023-09-23 15:36:32', NULL, NULL),
  (2, 9, 'TESTSEFDS', '1-LUKAS', '2023-09-23 15:38:08', NULL, NULL),
  (2, 10, 'EITA', '1-LUKAS', '2023-09-23 15:38:59', NULL, NULL),
  (2, 11, 'DBA', '1-LUKAS', '2023-09-28 21:48:41', NULL, NULL),
  (2, 12, 'TESTE', '1-LUKAS', '2023-09-28 21:53:17', NULL, NULL),
  (1, 5, 'TESE', '1-LUKAS', '2023-10-04 17:43:23', NULL, NULL),
  (1, 5, 'ADM SUPER', '1-LUKAS', '2023-10-04 18:16:00', NULL, NULL),
  (1, 6, 'ADM SUPER DOIS', '1-LUKAS', '2023-10-04 18:16:47', NULL, NULL),
  (2, 4, 'USER SUPER', '1-LUKAS', '2023-10-04 18:17:48', NULL, NULL);

-- Tabela pedido
CREATE TABLE IF NOT EXISTS pedido (
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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (tipo_pedido_id) REFERENCES opcoes (id),
  FOREIGN KEY (autor_usuario_id) REFERENCES usuario (id),
  FOREIGN KEY (prestador_usuario_id) REFERENCES usuario (id),
  FOREIGN KEY (status_pedido_id) REFERENCES opcoes (id)
);

-- Tabela tipo_usuario_tem_acesso_tela
CREATE TABLE IF NOT EXISTS tipo_usuario_tem_acesso_tela (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  acesso_tela_id INTEGER NOT NULL,
  tipo_usuario_id INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (acesso_tela_id) REFERENCES acesso_tela (id),
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes (id)
);

-- Tabela usuario
CREATE TABLE IF NOT EXISTS usuario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_usuario_id INTEGER NOT NULL,
  data_nascimento DATE NOT NULL,
  nome TEXT NOT NULL,
  email TEXT NOT NULL,
  email_status_id INTEGER NOT NULL,
  senha TEXT NOT NULL,
  cpf TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes (id)
);

"""
    cursor.executescript(sql)

    # Confirmar as alterações e fechar a conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
