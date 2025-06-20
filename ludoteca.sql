CREATE DATABASE IF NOT EXISTS ludoteca;
USE ludoteca;

#CATEGORIAS
CREATE TABLE `CATEGORIAS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
)

#PRODUCTOS
CREATE TABLE `PRODUCTOS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(255) NOT NULL,
  `PRECIO` int NOT NULL,
  `STOCK` int DEFAULT NULL,
  `DESCRIPCION` varchar(1000) NOT NULL,
  `CATEGORIA_ID` int,
  `IMAGEN` VARCHAR(255),
  PRIMARY KEY (`ID`),
  KEY `CATEGORIA_ID` (`CATEGORIA_ID`),
  CONSTRAINT `fk_produto_categoria_id`
        FOREIGN KEY (`CATEGORIA_ID`)
        REFERENCES `CATEGORIAS` (`ID`)
        ON DELETE SET NULL
);
#COMPRAS
CREATE TABLE `COMPRAS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `FECHA` datetime NOT NULL,
  `USUARIO_ID` int, -- Agregar not null y foreign key cuando sse agrega la tabla de usuarios
  `FINALIZADA` boolean,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `COMPRAS_PRODUCTOS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PRODUCTO_ID` int NOT NULL,
  `CANTIDAD` int NOT NULL,
  `COMPRA_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `PRODUCTO_ID` (`PRODUCTO_ID`),
  KEY `COMPRA_ID` (`COMPRA_ID`),
  CONSTRAINT PRODUCTO_COMPRA UNIQUE (PRODUCTO_ID,COMPRA_ID)
  CONSTRAINT `fk_compras_productos_compra_id` FOREIGN KEY (`COMPRA_ID`) REFERENCES `COMPRAS` (`ID`) ON DELETE CASCADE
  CONSTRAINT `fk_compras_productos_producto_id` FOREIGN KEY (`PRODUCTO_ID`) REFERENCES `PRODUCTOS` (`ID`) ON DELETE CASCADE
);

INSERT INTO `CATEGORIAS` (`NOMBRE`) VALUES 
('Infantil'),
('Familiar'),
('Adultos'),
('Fantasía'),
('Juego de rol'),
('Aprendizaje'),
('Estrategia');

INSERT INTO `PRODUCTOS` (`NOMBRE`,`PRECIO`,`STOCK`,`DESCRIPCION`,`CATEGORIA_ID`, `IMAGEN`) VALUES 
('TEG', 4000, null, 'Juego de estrategia por turnos de partidas de larga duracion', 4, 'images/gris.jpeg'),
('Ajedrez', 2500, null, 'El clásico juego de mesa etcetc', 7, '/images/ajedrez.jpg'),
('Monopoly', 3000, null, 'Ideal familia blablabla', 2, 'images/gris.jpeg'),
('D&D', 5000, null, 'Partidas largas de rol etcecte', 5, 'images/gris.jpeg'),
('4 en linea', 1500, null, 'hundir barcos y tal', 7, 'images/gris.jpeg'),
('UNO', 1000, null, 'para perder amistades y fragmentar a tu familia', 2, 'images/gris.jpeg'),
('Pictionary', 3500, null, 'Juego de dibujo familiar', 2, 'images/gris.jpeg'),
('Carrera de mente', 2000, null, 'Preguntas desafiantasnda', 6, 'images/gris.jpeg'),
('Damas', 2250, null, 'clasico etctec', 7, 'images/gris.jpeg'),
('Ludo', 1750, null, 'juego de familia muy familiar', 2, 'images/gris.jpeg'),
('Backgammon', 2199, null, 'azar y estrategia', 7, 'images/gris.jpeg'),
('Scrabble', 3200, null, 'Forma palabras para ganar', 6, 'images/gris.jpeg');


