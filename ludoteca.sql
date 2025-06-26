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

INSERT INTO `PRODUCTOS` (NOMBRE, PRECIO, STOCK, DESCRIPCION, RUBRO_ID) VALUES
('TEG', 4000, 10, 'Juego de estrategia por turnos donde los jugadores compiten por conquistar territorios en un mapa mundial. Ideal para sesiones largas y apasionantes entre amigos.', 4, 'images/teg.jpeg'),
('Ajedrez', 2500, 20, 'Clásico juego de mesa de origen milenario que enfrenta a dos jugadores en una batalla de lógica, concentración y estrategia pura.', 7,'images/ajedrez.jpeg'),
('Monopoly', 3000, 30, 'Divertido juego de compraventa de propiedades donde los jugadores compiten por construir imperios inmobiliarios y evitar la bancarrota.', 2, 'images/monopoly.png'),
('D&D', 5000, NULL, 'Juego de rol narrativo con dados y personajes personalizados. Ideal para quienes disfrutan de la fantasía, la imaginación y las aventuras en grupo.', 5, 'images/dnd.jpeg'),
('4 en línea', 1500, 5, 'Juego rápido y sencillo donde dos jugadores intentan alinear cuatro fichas del mismo color antes que su oponente. Perfecto para todas las edades.', 7, 'images/4linea.jpeg'),
('UNO', 1000, NULL, 'Juego de cartas dinámico y colorido, ideal para grupos. Las reglas simples esconden una divertida competencia cargada de sorpresas.', 2, 'images/uno.jpeg'),
('Pictionary', 3500, 30, 'Juego de mesa en el que los jugadores deben dibujar palabras o frases para que su equipo las adivine. Diversión asegurada para reuniones.', 2, 'images/pictionary.jpeg'),
('Carrera de mente', 2000, NULL, 'Desafiante juego de preguntas y respuestas que pone a prueba tu conocimiento general y rapidez mental en múltiples categorías.', 6, 'images/carreramente.jpeg'),
('Damas', 2250, 5, 'Juego de estrategia tradicional para dos jugadores donde el objetivo es capturar todas las piezas del oponente moviéndote en diagonal.', 7, 'images/damas.png'),
('Ludo', 1750, NULL, 'Clásico juego familiar en el que cada jugador compite por llevar sus fichas a la meta lanzando dados. Fácil de aprender y muy entretenido.', 2, 'images/ludo.jpeg'),
('Backgammon', 2199, 20, 'Juego de mesa de origen antiguo que combina azar y estrategia. El objetivo es ser el primero en sacar todas las fichas del tablero.', 7, 'images/backgammon.jpeg'),
('Scrabble', 3200, NULL, 'Juego de palabras cruzadas en el que se forman términos sobre un tablero para sumar puntos. Ideal para expandir vocabulario y divertirse.', 6, 'images/scrabble.jpeg');