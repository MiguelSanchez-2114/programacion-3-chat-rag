CREATE SCHEMA IF NOT EXISTS chat_rag_test;

CREATE TABLE IF NOT EXISTS chat_rag_test.usuario ( 
	id                   serial  NOT NULL  ,
	username             text  NOT NULL  ,
	"password"           text  NOT NULL  ,
	creado_en            timestamp DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT unq_usuario UNIQUE ( username ) ,
	CONSTRAINT pk_usuario PRIMARY KEY ( id )
 );

CREATE TABLE IF NOT EXISTS chat_rag_test.conversacion ( 
	id                   serial  NOT NULL  ,
	id_usuario           integer  NOT NULL  ,
	CONSTRAINT pk_conversacion PRIMARY KEY ( id ),
	CONSTRAINT fk_conversacion_usuario FOREIGN KEY ( id_usuario ) REFERENCES chat_rag_test.usuario( id )   
 );

COMMENT ON COLUMN chat_rag_test.conversacion.id_usuario IS 'Foreign key';

CREATE TABLE IF NOT EXISTS chat_rag_test.mensaje ( 
	id                   serial  NOT NULL  ,
	contenido            text  NOT NULL  ,
	emisor               text  NOT NULL  ,
	fecha                timestamp DEFAULT CURRENT_TIMESTAMP   ,
	id_conversacion      integer  NOT NULL  ,
	CONSTRAINT pk_mensaje PRIMARY KEY ( id ),
	CONSTRAINT fk_mensaje_conversacion FOREIGN KEY ( id_conversacion ) REFERENCES chat_rag_test.conversacion( id )   
 );

CREATE TABLE IF NOT EXISTS chat_rag_test.archivo ( 
	id                   serial  NOT NULL  ,
	nombre               text  NOT NULL  ,
	tipo                 text  NOT NULL  ,
	tamano               integer  NOT NULL  ,
	id_conversacion      integer  NOT NULL  ,
	CONSTRAINT pk_archivo PRIMARY KEY ( id ),
	CONSTRAINT unq_archivo_id_conversacion UNIQUE ( id_conversacion ) ,
	CONSTRAINT fk_archivo_id_conversacion FOREIGN KEY ( id_conversacion ) REFERENCES chat_rag_test.conversacion( id )   
 );