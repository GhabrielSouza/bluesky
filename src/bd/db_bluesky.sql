USE bluesky_db;

CREATE TABLE `postagens` (
  `id_postagens` int NOT NULL AUTO_INCREMENT,
  `cid` varchar(255) NOT NULL,
  `dataDeCriacao` datetime NOT NULL,
  `texto` text NOT NULL,
  `media` text DEFAULT NULL,
  `qtd_likes` int DEFAULT NULL,
  `qtd_repost` int DEFAULT NULL,
  `qtd_reply` int NOT NULL DEFAULT '0',
  `qtd_quote` int NOT NULL DEFAULT '0',
  `id_autores` int NOT NULL,
  `quote_to` int ,
  `reply_to` int ,
  PRIMARY KEY (`id_postagens`),
  KEY `fk_Postagens_quote_idx` (`quote_to`),
  KEY `fk_Postagens_reply_idx` (`reply_to`),
  KEY `fk_Postagens_Autores` (`id_autores`),
  CONSTRAINT `fk_Postagens_Autores` FOREIGN KEY (`id_autores`) REFERENCES `autores` (`id_autores`),
  CONSTRAINT `fk_Postagens_quote` FOREIGN KEY (`quote_to`) REFERENCES `postagens` (`id_postagens`),
  CONSTRAINT `fk_Postagens_reply` FOREIGN KEY (`reply_to`) REFERENCES `postagens` (`id_postagens`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `autores` (
  `id_autores` int NOT NULL AUTO_INCREMENT,
  `did` varchar(255) NOT NULL UNIQUE,
  `nome` text DEFAULT NULL,
  `handle` text DEFAULT NULL,
  PRIMARY KEY (`id_autores`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT * FROM autores;
SELECT * FROM postagens

