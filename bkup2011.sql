-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: umbrella
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acesso_tela`
--

DROP TABLE IF EXISTS `acesso_tela`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acesso_tela` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `url` varchar(100) NOT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `update_at` timestamp NULL DEFAULT NULL,
  `dateled_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acesso_tela`
--

LOCK TABLES `acesso_tela` WRITE;
/*!40000 ALTER TABLE `acesso_tela` DISABLE KEYS */;
INSERT INTO `acesso_tela` VALUES (1,'Informações Perfil','/perfil','1-LUKAS','2023-09-27 01:08:32',NULL,NULL,NULL,NULL),(2,'Opções','/opcoes','1-LUKAS','2023-09-27 01:08:56',NULL,NULL,NULL,NULL),(3,'Usuários','/usuarios','1-LUKAS','2023-09-27 01:51:05',NULL,NULL,NULL,NULL),(4,'Portfolio','/portfolio','1-LUKAS','2023-09-27 01:51:05',NULL,NULL,NULL,NULL),(5,'Meus Pedidos','/meus-pedidos','1-LUKAS','2023-09-27 01:51:05',NULL,NULL,NULL,NULL),(6,'Ajuda','/ajuda','1-LUKAS','2023-10-03 23:33:56',NULL,NULL,NULL,NULL),(7,'Acessos','/acessos','1-LUKAS','2023-10-04 18:55:23',NULL,NULL,NULL,NULL),(8,'Pedido','/pedido','1-LUKAS','2023-09-27 01:51:05',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `acesso_tela` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anexos`
--

DROP TABLE IF EXISTS `anexos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anexos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tabela` varchar(15) NOT NULL,
  `tabela_id` int NOT NULL,
  `nome` varchar(45) NOT NULL,
  `checksum` varchar(45) NOT NULL,
  `tipo` varchar(7) NOT NULL,
  `tamanho` int NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anexos`
--

LOCK TABLES `anexos` WRITE;
/*!40000 ALTER TABLE `anexos` DISABLE KEYS */;
INSERT INTO `anexos` VALUES (1,'usuario',1,'WhatsApp Image 2023-10-09 at 22.38.50','/10_2023/jWG29K4YM5vaYsMXbE5X.jpeg','.jpeg',64247,'1-LUKAS','2023-10-27 20:42:41',NULL,NULL,NULL,NULL),(2,'usuario',1,'100165295','/10_2023/nxXYSdw5mDybuPvEzX96.jfif','.jfif',20776,'1-LUKAS','2023-10-27 21:11:38',NULL,NULL,NULL,NULL),(3,'usuario',8,'WhatsApp Image 2023-10-27 at 17.26.33','/10_2023/PNtd8drLlpQRd9nynMfp.jpeg','.jpeg',97277,'1-LUKAS','2023-10-27 21:28:06',NULL,NULL,NULL,NULL),(4,'usuario',4,'WhatsApp Image 2023-10-27 at 17.26.55','/10_2023/sihze2yratgoGMSaIyJG.jpeg','.jpeg',85320,'8-SILVIA','2023-10-27 21:29:09',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `anexos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cobranca`
--

DROP TABLE IF EXISTS `cobranca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cobranca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `status_cobranca_id` int NOT NULL,
  `forma_pagamento_id` int NOT NULL,
  `descricao` varchar(45) NOT NULL,
  `valor` decimal(16,2) NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cobranca_pedido1` (`pedido_id`),
  KEY `fk_cobranca_opcoes1` (`forma_pagamento_id`),
  KEY `fk_cobranca_opcoes2` (`status_cobranca_id`),
  CONSTRAINT `fk_cobranca_opcoes1` FOREIGN KEY (`forma_pagamento_id`) REFERENCES `opcoes` (`id`),
  CONSTRAINT `fk_cobranca_opcoes2` FOREIGN KEY (`status_cobranca_id`) REFERENCES `opcoes` (`id`),
  CONSTRAINT `fk_cobranca_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobranca`
--

LOCK TABLES `cobranca` WRITE;
/*!40000 ALTER TABLE `cobranca` DISABLE KEYS */;
/*!40000 ALTER TABLE `cobranca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cores`
--

DROP TABLE IF EXISTS `cores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `codigo_hexadecimal` varchar(7) NOT NULL,
  `ordem` int NOT NULL,
  `descricao` varchar(45) NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cores_pedido` (`pedido_id`),
  CONSTRAINT `fk_cores_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cores`
--

LOCK TABLES `cores` WRITE;
/*!40000 ALTER TABLE `cores` DISABLE KEYS */;
/*!40000 ALTER TABLE `cores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fila_email`
--

DROP TABLE IF EXISTS `fila_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fila_email` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(20) NOT NULL,
  `mensagem` varchar(200) NOT NULL,
  `email_envio` varchar(45) NOT NULL,
  `para_usuario_id` int DEFAULT NULL,
  `tipo_email_id` int NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_fila_email_opcoes1_idx` (`tipo_email_id`),
  CONSTRAINT `fk_fila_email_opcoes1` FOREIGN KEY (`tipo_email_id`) REFERENCES `opcoes` (`id`),
  CONSTRAINT `fk_fila_email_usuario1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fila_email`
--

LOCK TABLES `fila_email` WRITE;
/*!40000 ALTER TABLE `fila_email` DISABLE KEYS */;
/*!40000 ALTER TABLE `fila_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opcoes`
--

DROP TABLE IF EXISTS `opcoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opcoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `grupo` int NOT NULL,
  `item` int NOT NULL,
  `descricao` varchar(45) NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes`
--

LOCK TABLES `opcoes` WRITE;
/*!40000 ALTER TABLE `opcoes` DISABLE KEYS */;
INSERT INTO `opcoes` VALUES (1,1,1,'GRUPO DE OPÇÕES','1-LUKAS','2023-09-16 00:45:55',NULL,NULL,NULL,NULL),(2,1,2,'TIPOS DE USUÁRIO','1-LUKAS','2023-09-16 00:45:55',NULL,NULL,NULL,NULL),(3,2,1,'ADMINISTRADOR','1-LUKAS','2023-09-16 00:45:55',NULL,NULL,NULL,NULL),(4,2,2,'CLIENTE','1-LUKAS','2023-09-16 00:45:55',NULL,NULL,NULL,NULL),(5,2,3,'PRESTADOR DE SERVIÇO','1-LUKAS','2023-09-16 00:45:55',NULL,NULL,NULL,NULL),(6,1,3,'TIPOS DE EMAIL.','1-LUKAS','2023-09-19 21:07:56','1-LUKAS','2023-10-27 14:39:27',NULL,NULL),(7,3,1,'CRIAR CONTA','1-LUKAS','2023-09-19 21:08:12',NULL,NULL,NULL,NULL),(8,1,4,'STATUS EMAIL USUÁRIOS','1-LUKAS','2023-09-19 21:40:19','1-LUKAS','2023-10-04 21:51:13',NULL,NULL),(9,4,1,'VERIFICADO','1-LUKAS','2023-09-19 21:40:42',NULL,NULL,NULL,NULL),(10,4,2,'NÃO VERIFICADO','1-LUKAS','2023-09-19 21:40:42',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `opcoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_pedido_id` int NOT NULL,
  `autor_usuario_id` int NOT NULL,
  `prestador_usuario_id` int NOT NULL,
  `status_pedido_id` int NOT NULL,
  `titulo` varchar(45) NOT NULL,
  `subtituto` varchar(45) NOT NULL,
  `outros_detalhes` varchar(2000) DEFAULT NULL,
  `redes_sociais_referencia` varchar(150) DEFAULT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pedido_usuario_autor` (`autor_usuario_id`),
  KEY `fk_pedido_usuario_prestador` (`prestador_usuario_id`),
  KEY `fk_pedido_opcoes1` (`status_pedido_id`),
  KEY `fk_pedido_opcoes2` (`tipo_pedido_id`),
  CONSTRAINT `fk_pedido_opcoes1` FOREIGN KEY (`status_pedido_id`) REFERENCES `opcoes` (`id`),
  CONSTRAINT `fk_pedido_opcoes2` FOREIGN KEY (`tipo_pedido_id`) REFERENCES `opcoes` (`id`),
  CONSTRAINT `fk_pedido_usuario_autor` FOREIGN KEY (`autor_usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `fk_pedido_usuario_prestador` FOREIGN KEY (`prestador_usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_usuario_tem_acesso_tela`
--

DROP TABLE IF EXISTS `tipo_usuario_tem_acesso_tela`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario_tem_acesso_tela` (
  `id` int NOT NULL AUTO_INCREMENT,
  `acesso_tela_id` int NOT NULL,
  `tipo_usuario_id` int NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `acesso_tela_id` (`acesso_tela_id`),
  KEY `tipo_usuario_id` (`tipo_usuario_id`),
  CONSTRAINT `tipo_usuario_tem_acesso_tela_ibfk_1` FOREIGN KEY (`acesso_tela_id`) REFERENCES `acesso_tela` (`id`),
  CONSTRAINT `tipo_usuario_tem_acesso_tela_ibfk_2` FOREIGN KEY (`tipo_usuario_id`) REFERENCES `opcoes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_usuario_tem_acesso_tela`
--

LOCK TABLES `tipo_usuario_tem_acesso_tela` WRITE;
/*!40000 ALTER TABLE `tipo_usuario_tem_acesso_tela` DISABLE KEYS */;
INSERT INTO `tipo_usuario_tem_acesso_tela` VALUES (1,1,1,'1-LUKAS','2023-10-28 13:56:08',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `tipo_usuario_tem_acesso_tela` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_usuario_id` int NOT NULL,
  `data_nascimento` date NOT NULL,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `email_status_id` int NOT NULL,
  `senha` varchar(45) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_usuario_tipo_usuario` (`tipo_usuario_id`),
  KEY `fk_email_status_usuario_idx` (`email_status_id`),
  CONSTRAINT `fk_usuario_tipo_usuario` FOREIGN KEY (`tipo_usuario_id`) REFERENCES `opcoes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,1,'2003-12-08','LUKAS ROCHA RODRIGUES','lkscomk@gmail.com',2,'20030714','04718450276','1-LUKAS','2023-09-16 19:31:23','1-LUKAS','2023-10-27 21:11:37',NULL,NULL),(2,2,'1996-06-04','ERICK THIAGO','erickthiago@gmil.com',2,'teste123','03118732270','1-LUKAS','2023-09-16 19:37:19','1-LUKAS','2023-10-04 13:39:39',NULL,NULL),(3,1,'1986-08-17','MAGNO','magnosib5@gmail.com',2,'12345678','12374564749','1-LUKAS','2023-09-19 03:21:42',NULL,NULL,NULL,NULL),(4,1,'2003-12-08','MARINA REGINATO','reginato0909@gmail.com',2,'123456789','04718450276','1-LUKAS','2023-09-19 03:24:51','8-SILVIA','2023-10-27 21:29:08',NULL,NULL),(5,2,'1971-01-04','ADRIANA ZANKI','Adrianazanki@gmail.com',2,'12345678','03118732270','1-LUKAS','2023-09-19 04:27:53',NULL,NULL,NULL,NULL),(6,2,'1996-02-29','MARIA','tsi.bethy@gmail.com',2,'bethy1234','12345789789','1-LUKAS','2023-09-26 03:13:32',NULL,NULL,NULL,NULL),(7,2,'2003-09-03','GETÚLIO','getuliowerle@gmail.com',2,'19357122Gg','59546546813','1-LUKAS','2023-09-28 03:29:27',NULL,NULL,NULL,NULL),(8,1,'2000-01-01','SILVIA PATRICIA','silviapsg93@gmail.com',2,'123456789','03118732270','1-LUKAS','2023-10-27 21:23:03','1-LUKAS','2023-10-27 21:28:05',NULL,NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-20 16:08:29

ALTER TABLE `umbrella`.`acesso_tela`
CHANGE COLUMN `deleted_by` `deleted_by` VARCHAR(45) NULL DEFAULT NULL ;


ALTER TABLE `umbrella`.`acesso_tela`
CHANGE COLUMN `update_at` `updated_at` TIMESTAMP NULL DEFAULT NULL ;
