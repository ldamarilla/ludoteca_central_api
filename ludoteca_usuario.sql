CREATE DATABASE IF NOT EXISTS ludoteca_usuario;
USE ludoteca_usuario;

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

CREATE TABLE `TOKEN_USUARIO` (
  `TOKEN` VARCHAR (255) PRIMARY KEY,
  `ID_USUARIO` INT NOT NULL,
  FOREIGN KEY (`ID_USUARIO`) REFERENCES `USUARIO`(`ID_USUARIO`)
);
                                                                                         
INSERT INTO `USUARIO`(NOMBRE,EMAIL,CONTRASENIA,ADMIN) VALUES ('Admin','admin@gmail.com','12345', 1);

