CREATE DATABASE IF NOT EXISTS ludoteca;
USE ludoteca;

# CATEGORIAS
CREATE TABLE `CATEGORIAS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
);

# USUARIO
CREATE TABLE `USUARIO` (
  `ID_USUARIO` int NOT NULL AUTO_INCREMENT,
  `EMAIL` varchar(255) NOT NULL,
  `CONTRASENIA` varchar(255) NOT NULL,
  `NOMBRE` varchar(255) NULL,
  `DIRECCION` varchar(255) NULL,
  `PISO` int NULL,
  `TIMBRE` varchar(10) NULL,
  `APELLIDO` varchar(255) NULL,
  `DNI` int NULL,
  `ADMIN` boolean,
  PRIMARY KEY (`ID_USUARIO`)
);

# PRODUCTOS
CREATE TABLE `PRODUCTOS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(255) NOT NULL,
  `PRECIO` int NOT NULL,
  `STOCK` int DEFAULT NULL,
  `DESCRIPCION` varchar(1000) NOT NULL,
  `CATEGORIA_ID` int,
  `IMAGEN` LONGTEXT,
  PRIMARY KEY (`ID`),
  KEY `CATEGORIA_ID` (`CATEGORIA_ID`),
  CONSTRAINT `fk_produto_categoria_id`
        FOREIGN KEY (`CATEGORIA_ID`)
        REFERENCES `CATEGORIAS` (`ID`)
        ON DELETE SET NULL
);

# COMPRAS
CREATE TABLE `COMPRAS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `FECHA` datetime NOT NULL,
  `USUARIO_ID` int,
  `FINALIZADA` boolean,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_compras_usuario_id` FOREIGN KEY (`USUARIO_ID`) REFERENCES `USUARIO`(`ID_USUARIO`) ON DELETE SET NULL
);

CREATE TABLE `COMPRAS_PRODUCTOS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PRODUCTO_ID` int NOT NULL,
  `CANTIDAD` int NOT NULL,
  `COMPRA_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `PRODUCTO_ID` (`PRODUCTO_ID`),
  KEY `COMPRA_ID` (`COMPRA_ID`),
  CONSTRAINT PRODUCTO_COMPRA UNIQUE (PRODUCTO_ID,COMPRA_ID),
  CONSTRAINT `fk_compras_productos_compra_id` FOREIGN KEY (`COMPRA_ID`) REFERENCES `COMPRAS` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_compras_productos_producto_id` FOREIGN KEY (`PRODUCTO_ID`) REFERENCES `PRODUCTOS` (`ID`) ON DELETE CASCADE
);

CREATE TABLE `TOKEN_USUARIO` (
  `TOKEN` VARCHAR (255) PRIMARY KEY,
  `ID_USUARIO` INT NOT NULL,
  FOREIGN KEY (`ID_USUARIO`) REFERENCES `USUARIO`(`ID_USUARIO`)
);

# PEDIDOS
CREATE TABLE `PEDIDOS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PRODUCTO_ID` int NOT NULL,
  `COMPRAS_ID` int NOT NULL,
  `USUARIO_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_pedidos_producto_id` FOREIGN KEY (`PRODUCTO_ID`)
		REFERENCES `PRODUCTOS`(`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pedidos_compra_id` FOREIGN KEY (`COMPRAS_ID`)
		REFERENCES `COMPRAS`(`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pedidos_compra_usuario_id` FOREIGN KEY (`USUARIO_ID`)
        REFERENCES `USUARIO`(`ID_USUARIO`) ON DELETE CASCADE
);

# Inserciones

INSERT INTO `USUARIO`(NOMBRE,EMAIL,CONTRASENIA,ADMIN) VALUES ('Admin','admin@gmail.com','12345', 1);

INSERT INTO `CATEGORIAS` (`NOMBRE`) VALUES 
('Infantil'),
('Familiar'),
('Adultos'),
('Fantasía'),
('Juego de rol'),
('Aprendizaje'),
('Estrategia');

INSERT INTO `PRODUCTOS` (`NOMBRE`,`PRECIO`,`STOCK`,`DESCRIPCION`,`CATEGORIA_ID`, `IMAGEN`) VALUES 
('TEG', 4000, 10, 'Juego de estrategia por turnos de partidas de larga duracion', 4, 'images/teg.jpeg'),
('Ajedrez', 2500, 10, 'El clásico juego de mesa etcetc', 7, 'images/ajedrez.jpeg'),
('Monopoly', 3000, 10, 'Ideal familia blablabla', 2, 'images/monopoly.png'),
('D&D', 5000, 10, 'Partidas largas de rol etcecte', 5, 'images/dnd.jpeg'),
('4 en linea', 1500, 10, 'hundir barcos y tal', 7, 'images/4linea.jpeg'),
('UNO', 1000, 10, 'para perder amistades y fragmentar a tu familia', 2, 'images/uno.jpeg'),
('Pictionary', 3500, 10, 'Juego de dibujo familiar', 2, 'images/pictionary.jpeg'),
('Carrera de mente', 2000, 10, 'Preguntas desafiantasnda', 6, 'images/carreramente.jpeg'),
('Damas', 2250, 10, 'clasico etctec', 7, 'images/damas.png'),
('Ludo', 1750, 10, 'juego de familia muy familiar', 2, 'images/ludo.jpeg'),
('Backgammon', 2199, 10, 'azar y estrategia', 7, 'images/backgammon.jpeg'),
('Scrabble', 3200, 10, 'Forma palabras para ganar', 6, 'images/scrabble.jpeg');



