CREATE TABLE provincias (
	id_provincia int8 NOT NULL PRIMARY KEY,
	provincia varchar(150) NOT NULL,
	fecha timestamp
);

CREATE TABLE espacios (
	id int8 NOT NULL PRIMARY KEY,
	cod_localidad int4 NULL,
	id_provincia int4  NOT NULL,
    id_departamento int4 NULL,
	categoria varchar(100) NULL,
	localidad varchar(200) NULL,
	nombre varchar(300) NULL,
	domicilio varchar(300) NULL,
	codigo_postal varchar(10) null,
	telefono varchar(300) NULL,
	mail varchar(300) NULL,
	web varchar(300) NULL,
	fecha timestamp,
	constraint fk_provincia foreign key(id_provincia) references
	provincias(id_provincia)
	);



