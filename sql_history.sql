/* ### psql ###
Historial de querys postgreSQL para carga de datos.
*/
--||| (usando usr = postgres) |||--
-- Usuario
CREATE USER editor_en WITH PASSWORD 'editarend24';

-- Base de datos
CREATE DATABASE endnote_refs OWNER editor_en;
GRANT ALL PRIVILEGES ON DATABASE endnote_refs TO editor_en;

--||| (con usr = editor_en) |||--
-- esquema
CREATE SCHEMA endnote;

-- CREATE TABLE - con psycopg2 (load.py)

-- setear para ver tablas de esquema "endnote"
--  (sino por defecto aparecen los del esquema "public")

-- !!!! NOTA: necesario ejecutar en cada sesión...
SET search_path TO endnote;

-- INSERT con psycopg2 (load.py)
/*
    NOTA:   Funcionó, puedo visualizar los datos en DBaver
            sin embargo, psql tiene algún problema con la
            codificación del texto en la tabla.
            Tal vez tenga que ver con el mensaje de error en psql de W:

            "ADVERTENCIA: El código de página de la consola (850) difiere del código
                        de página de Windows (1252).
                        Los caracteres de 8 bits pueden funcionar incorrectamente.
                        Vea la página de referencia de psql «Notes for Windows users»
                        para obtener más detalles".
*/

-- Solucionar error de codificación psql:
SELECT pg_encoding_to_char(encoding) FROM pg_database WHERE datname = 'endnote_refs';

-- permite evitar error, sin embargo imprime los registros sin un formato legible (cualquier cantidad
-- de saltos de página sin sentido):
SET client_encoding = 'UTF8';

/*Conclusión (por ahora al menos)
    USANDO : editor SQL de DBaver y consultas en python/psycopg2 
        (ver load.py, query_sql)
*/

-- En DBeaver               --

select * from endnote_refs.endnote.referencias;

select condoi.tipo, COUNT(*) as con_DOI from (select * 
		from endnote_refs.endnote.referencias 
		where doi is not null) as condoi
		group by condoi.tipo;
		
select condoi.tipo, COUNT(*) as DOI_nulos from (select * 
		from endnote_refs.endnote.referencias 
		where doi is null) as condoi
		group by condoi.tipo;

select tipo, COUNT(*) as n
		from endnote_refs.endnote.referencias
		group by tipo;





-- Contar años erroneos
SELECT tipo,
       COUNT(CASE WHEN LENGTH(año) > 4 THEN 1 END) AS errores, -- 1 es solo por que hay que poner algo (evaua que sea verdadero)
       COUNT(CASE WHEN LENGTH(año) <= 4 THEN 1 END) AS correctos,
       COUNT(*) AS n
FROM endnote_refs.endnote.referencias
GROUP BY tipo;

-- Ver años erroneos por tipo de registro
select * from endnote_refs.endnote.referencias
		where LENGTH(año) > 4;

-- Reparar años con errores de tipeo:
UPDATE endnote.referencias
	SET año='1998'
	WHERE nregistro=1774;
UPDATE endnote.referencias
	SET año='2001'
	WHERE nregistro=2795;
UPDATE endnote.referencias
	SET año='1985'
	WHERE nregistro=1474;
UPDATE endnote.referencias
	SET año='1979'
	WHERE nregistro=544;
UPDATE endnote.referencias
	SET año='1994'
	WHERE nregistro=274;
UPDATE endnote.referencias
	SET año='2000'
	WHERE nregistro=1059;
UPDATE endnote.referencias
	SET año='1988'
	WHERE nregistro=333;
UPDATE endnote.referencias
	SET año='1981'
	WHERE nregistro=551;
UPDATE endnote.referencias
	SET año='1992'
	WHERE nregistro=2849;
UPDATE endnote.referencias
	SET año='2003'
	WHERE nregistro=2895;
UPDATE endnote.referencias
	SET año='2006'
	WHERE nregistro=3029;
UPDATE endnote.referencias
	SET año='1966'
	WHERE nregistro=1700;

-- Verificar 

select año, count(*)  from endnote.referencias
	where LENGTH(año) = 4
	group by año;

select COUNT(*) from endnote.referencias
	where LENGTH(año) = 4;

select COUNT(*) from endnote.referencias;

-- solo dos nulos
select nregistro, año, titulo from endnote.referencias
	where año is null;

-- !! cast a int
ALTER TABLE endnote.referencias
ALTER COLUMN año TYPE INTEGER USING año::INTEGER;


select * from endnote.referencias where año > 1500;

-- Ver cuales no tienen doi y son de este siglo:

select * from endnote.referencias 
	where 
		año > 2000 and
		doi is not null;

select count(*) from endnote.referencias 
	where 
		año > 2000 and
		doi is not null;
 
select tipo, count(*) from endnote.referencias 
	where 
		año > 2000 and
		doi is not null
	group by tipo;
	
select * from endnote.referencias 
	where 
		año > 2000 and
		doi is not null and
		tipo = 'Catalog';

select titulo, autores, año, editorial from endnote.referencias 
	where 
		año > 2000 and
		doi is null and
		tipo = 'Book Section';

select * from endnote.referencias 
	where 
		año > 2000 and
		doi is null and
		tipo = 'Journal Article';
	
select * from endnote.referencias
	where 
		titulo like '%daptation of hemocyanin within spi%';
		
select nregistro , titulo from endnote.referencias where nregistro = 3520;

select nregistro, titulo from endnote.referencias 
    where 
        año > 2000 and
        doi is null and
        tipo = 'Journal Article';
       

select count(*)  from endnote.referencias 
    where 
        año > 2000 and
        doi is null and
        tipo = 'Journal Article';
       
select * from endnote.referencias where titulo = 'Chlorpyrifos';
       
       

/*----- pruebas de inserción de DOI -----*/
-- Tabla

create table if not exists endnote.busqueda_doi (
	nregistro INTEGER NOT NULL PRIMARY KEY,        
	titulo VARCHAR(440),
	doi_nuevo VARCHAR(125)
);

select * from endnote.busqueda_doi;
select COUNT(*) as n from endnote.busqueda_doi
where doi_nuevo ='no hallado';
select * from endnote.referencias r  where titulo = 'Chlorpyrifos';
-- !!!!!
-- delete from endnote.busqueda_doi;
-- !!!!!

-- muestrar el 25% de filas
SELECT * 
FROM endnote.busqueda_doi 
ORDER BY RANDOM() 
LIMIT (SELECT COUNT(*) * 0.25 FROM endnote.busqueda_doi); -- solo calcula el 25%

SELECT * 
FROM endnote.busqueda_doi 
where doi_nuevo <> 'no hallado'
ORDER BY RANDOM() 
LIMIT (SELECT COUNT(*) * 0.25 FROM endnote.busqueda_doi); -- solo calcula el 25%



SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'endnote'
  AND table_name = 'busqueda_doi';

select * 
from endnote.busqueda_doi;

create table if not exists endnote.rev_doi_j (
            nregistro INTEGER NOT NULL PRIMARY KEY,        
            titulo VARCHAR(440),
            crossref_tit VARCHAR(440),
            doi_nuevo VARCHAR(125)
            );

select  * from endnote.rev_doi_j rdj;

COMMENT ON DATABASE endnote_refs 
IS 'Referencias extraídas de biblioteca de EndNote, actualizadas con API de Crossref a través de Python.';

select * from endnote.busqueda_doi 
    where 
        doi_nuevo != 'no hallado';

select bd.titulo as encontrado, r.titulo as tit_en_EN, r.doi as insertado, bd.doi_nuevo
	from 
		endnote.rev_doi_j bd
    inner join 
    	endnote.referencias r ON bd.nregistro = r.nregistro
    where 
       bd.doi_nuevo != 'no hallado';

-- anda, no sé por qué marca error en bd...      
UPDATE endnote.referencias r
SET doi = bd.doi_nuevo
from   (select nregistro, doi_nuevo
		from endnote.busqueda_doi
		where doi_nuevo != 'no hallado') as bd
where 
		bd.nregistro = r.nregistro;

select doi, titulo from endnote.referencias r 
where doi is null;

