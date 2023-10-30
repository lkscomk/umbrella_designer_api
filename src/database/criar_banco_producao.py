import sqlite3
import os

# Nome do arquivo de banco de dados SQLite
banco = arquivo = f'{os.path.dirname(os.path.abspath(__file__))}/banco.db'

# Função para criar as tabelas
def criar_tabelas():
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()

    sql = """
-- Definição da tabela 'acesso_tela'
CREATE TABLE IF NOT EXISTS acesso_tela (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  url TEXT NOT NULL,
  created_by TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  update_at TIMESTAMP,
  dateled_by TEXT,
  deleted_at TIMESTAMP
);

-- Definição da tabela 'anexos'
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
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP
);

-- Definição da tabela 'cobranca'
CREATE TABLE IF NOT EXISTS cobranca (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  status_cobranca_id INTEGER NOT NULL,
  forma_pagamento_id INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  valor NUMERIC(16, 2) NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP,
  FOREIGN KEY (forma_pagamento_id) REFERENCES opcoes (id),
  FOREIGN KEY (status_cobranca_id) REFERENCES opcoes (id),
  FOREIGN KEY (pedido_id) REFERENCES pedido (id)
);

-- Definição da tabela 'cores'
CREATE TABLE IF NOT EXISTS cores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  codigo_hexadecimal TEXT NOT NULL,
  ordem INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP,
  FOREIGN KEY (pedido_id) REFERENCES pedido (id)
);

-- Definição da tabela 'fila_email'
CREATE TABLE IF NOT EXISTS fila_email (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  mensagem TEXT NOT NULL,
  email_envio TEXT NOT NULL,
  para_usuario_id INTEGER,
  tipo_email_id INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP,
  FOREIGN KEY (tipo_email_id) REFERENCES opcoes (id),
  FOREIGN KEY (para_usuario_id) REFERENCES usuario (id)
);

-- Criação da tabela
CREATE TABLE IF NOT EXISTS opcoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grupo INTEGER NOT NULL,
  item INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP
);

-- Definição da tabela 'pedido'
CREATE TABLE IF NOT EXISTS pedido (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL,
  data_pedido DATE NOT NULL,
  numero_pedido INTEGER NOT NULL,
  quantidade_total INTEGER NOT NULL,
  valor_total NUMERIC(16, 2) NOT NULL,
  status_pedido_id INTEGER NOT NULL,
  data_faturamento DATE,
  data_envio DATE,
  data_entrega DATE,
  endereco_entrega TEXT,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuario (id),
  FOREIGN KEY (status_pedido_id) REFERENCES opcoes (id)
);

-- Criação da tabela
CREATE TABLE IF NOT EXISTS tipo_usuario_tem_acesso_tela (
  id INTEGER PRIMARY KEY,
  acesso_tela_id INTEGER NOT NULL,
  tipo_usuario_id INTEGER NOT NULL,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP,
  deleted_by TEXT,
  deleted_at TIMESTAMP,
  FOREIGN KEY (acesso_tela_id) REFERENCES acesso_tela (id),
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes (id)
);

-- Criação da tabela usuario
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
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT DEFAULT NULL,
  updated_at DATETIME DEFAULT NULL,
  deleted_by TEXT DEFAULT NULL,
  deleted_at DATETIME DEFAULT NULL,
  FOREIGN KEY (tipo_usuario_id) REFERENCES opcoes (id)
);

-- Dados da tabela 'acesso_tela'
INSERT INTO acesso_tela (nome, url, created_by, created_at, updated_by, update_at, dateled_by, deleted_at) VALUES
  ('Informações Perfil', '/perfil', '1-LUKAS', '2023-09-26 21:08:32', NULL, NULL, NULL, NULL),
  ('Opções', '/opcoes', '1-LUKAS', '2023-09-26 21:08:56', NULL, NULL, NULL, NULL),
  ('Usuários', '/usuarios', '1-LUKAS', '2023-09-26 21:51:05', NULL, NULL, NULL, NULL),
  ('Portfolio', '/portfolio', '1-LUKAS', '2023-09-26 21:51:05', NULL, NULL, NULL, NULL),
  ('Meus Pedidos', '/meus-pedidos', '1-LUKAS', '2023-09-26 21:51:05', NULL, NULL, NULL, NULL),
  ('Pedido', '/pedido', '1-LUKAS', '2023-09-26 21:51:05', NULL, NULL, NULL, NULL),
  ('Ajuda', '/ajuda', '1-LUKAS', '2023-10-03 19:33:56', NULL, NULL, NULL, NULL),
  ('Acessos', '/acessos', '1-LUKAS', '2023-10-04 14:55:23', NULL, NULL, NULL, NULL);

-- Dados da tabela 'anexos'
INSERT INTO anexos (tabela, tabela_id, nome, checksum, tipo, tamanho, created_by, created_at, updated_by, updated_at, deleted_by, deleted_at) VALUES
  ('usuario', 1, 'WhatsApp Image 2023-10-09 at 22.38.50', '/10_2023/jWG29K4YM5vaYsMXbE5X.jpeg', '.jpeg', 64247, '1-LUKAS', '2023-10-27 20:42:41', NULL, NULL, NULL, NULL),
  ('usuario', 1, '100165295', '/10_2023/nxXYSdw5mDybuPvEzX96.jfif', '.jfif', 20776, '1-LUKAS', '2023-10-27 21:11:38', NULL, NULL, NULL, NULL),
  ('usuario', 8, 'WhatsApp Image 2023-10-27 at 17.26.33', '/10_2023/PNtd8drLlpQRd9nynMfp.jpeg', '.jpeg', 97277, '1-LUKAS', '2023-10-27 21:28:06', NULL, NULL, NULL, NULL),
  ('usuario', 4, 'WhatsApp Image 2023-10-27 at 17.26.55', '/10_2023/sihze2yratgoGMSaIyJG.jpeg', '.jpeg', 85320, '8-SILVIA', '2023-10-27 21:29:09', NULL, NULL, NULL, NULL),
  ('usuario', 3, 'WhatsApp Image 2023-10-27 at 17.26.55', '/10_2023/Nv2Suq4RNudyg7UVEXEf.jpeg', '.jpeg', 85320, '3-MAGNO', '2023-10-27 21:29:09', NULL, NULL, NULL, NULL);

-- Inserção de dados
INSERT INTO opcoes (grupo, item, descricao, created_by, created_at, updated_by, updated_at, deleted_by, deleted_at) VALUES
(1, 1, 'GRUPO DE OPÇÕES', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL, NULL, NULL),
(1, 2, 'TIPOS DE USUÁRIO', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL, NULL, NULL),
(2, 1, 'ADMINISTRADOR', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL, NULL, NULL),
(2, 2, 'CLIENTE', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL, NULL, NULL),
(2, 3, 'PRESTADOR DE SERVIÇO', '1-LUKAS', '2023-09-16 00:45:55', NULL, NULL, NULL, NULL),
(1, 3, 'TIPOS DE EMAIL.', '1-LUKAS', '2023-09-19 21:07:56', '1-LUKAS', '2023-10-27 14:39:27', NULL, NULL),
(3, 1, 'CRIAR CONTA', '1-LUKAS', '2023-09-19 21:08:12', NULL, NULL, NULL, NULL),
(1, 4, 'STATUS EMAIL USUÁRIOS', '1-LUKAS', '2023-09-19 21:40:19', '1-LUKAS', '2023-10-04 21:51:13', NULL, NULL),
(4, 1, 'VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42', NULL, NULL, NULL, NULL),
(4, 2, 'NÃO VERIFICADO', '1-LUKAS', '2023-09-19 21:40:42', NULL, NULL, NULL, NULL);

-- Inserção de dados
INSERT INTO tipo_usuario_tem_acesso_tela (acesso_tela_id, tipo_usuario_id, created_by, created_at, updated_by, updated_at, deleted_by, deleted_at)
VALUES (1,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (1,2,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (1,3,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (2,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (3,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (10,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (3,3,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,'1-LUKAS','2023-10-04 12:02:00'),
       (4,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (4,2,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (4,3,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (5,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (5,2,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (6,1,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (6,2,'1-LUKAS','0000-00-00 00:00:00',NULL,NULL,NULL,NULL),
       (9,1,'1-LUKAS','2023-10-28 11:27:54',NULL,NULL,NULL,NULL),
       (9,2,'1-LUKAS','2023-10-28 11:34:45',NULL,NULL,NULL,NULL),
       (5,3,'1-LUKAS','2023-10-28 11:35:30',NULL,NULL,NULL,NULL),
       (6,3,'1-LUKAS','2023-10-28 11:35:30',NULL,NULL,NULL,NULL);

-- Inserção de dados na tabela usuario
INSERT INTO usuario (tipo_usuario_id, data_nascimento, nome, email, email_status_id, senha, cpf, created_by, created_at)
VALUES
  (1, '2003-07-15', 'LUKAS RODRIGUES', 'lkscomk@gmail.com', 2, '20030714', '03118732270', '1-LUKAS', '2023-09-16 19:31:23'),
  (2, '1996-06-04', 'ERICK THIAGO', 'erickthiago@gmil.com', 2, 'teste123', '03118732270', '1-LUKAS', '2023-09-16 19:37:19'),
  (2, '1986-08-17', 'MAGNO', 'magnosib5@gmail.com', 2, '12345678', '12374564749', '1-LUKAS', '2023-09-19 03:21:42'),
  (3, '2003-12-08', 'MARINA REGINATO', 'reginato0909@gmail.com', 2, '123456789', '04718450276', '1-LUKAS', '2023-09-19 03:24:51'),
  (2, '1971-01-04', 'ADRIANA ZANKI', 'Adrianazanki@gmail.com', 2, '12345678', '03118732270', '1-LUKAS', '2023-09-19 04:27:53'),
  (2, '1996-02-29', 'MARIA', 'tsi.bethy@gmail.com', 2, 'bethy1234', '12345789789', '1-LUKAS', '2023-09-26 03:13:32'),
  (2, '2003-09-03', 'GETÚLIO', 'getuliowerle@gmail.com', 2, '19357122Gg', '59546546813', '1-LUKAS', '2023-09-28 03:29:27'),
  (1, '2000-01-01', 'SILVIA PATRICIA', 'silviapsg93@gmail.com',2,'123456789','03118732270','1-LUKAS','2023-10-27 21:23:03');
"""

    cursor.executescript(sql)
    # Confirmar as alterações e fechar a conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
