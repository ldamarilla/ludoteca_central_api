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
  PRIMARY KEY (`ID_USUARIO`)
)