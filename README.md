# Limpiar y completar Biblioteca de Endnote

Archivo principal de ejecución **[main.py](main.py)** con orquestación del *pipeline*.  
Archivo con historial SQL **[sql_history.sql](sql_history.sql)** de cambios a los datos.

## 1. Extraer datos desde .xml y cargarlos a una tabla postgreSQL
### Archivos Extracción /[extraer_desde_Xml](extraer_desde_xml)
Usado paquete `xml.etree.ElementTree` para *parsear* el archivo .xml generado desde Endnote
### Archivos carga a DB /[Carga a postgreSQL](carga_posgres)
Se empleó psql, y el módulo de python.

---
    base de datos: endnote_refs
    usuario: editor_en
    servidor: localhost
    port: 5432
----
## 2. Crear app para buscar por título los DOI que faltan (API de crossref) e insertarlos en su respectiva columna de la tabla.
Uso de API de [CrossRef](https://search.crossref.org/), con librerias de python. Pruebas con:

Probado y descartado:

    pip install crossrefapi

Empleado al final [pag](https://pypi.org/project/habanero/)

    pip install habanero

## 3. Crear app para reinsertar todos los registros en una nueva biblioteca de Endnote (en windows obligatoriamente)