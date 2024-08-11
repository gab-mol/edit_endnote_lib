# Limpiar y completar Biblioteca de Endnote

***---EN PROCESO---***

Archivo principal de ejecución **[main.ipynb](main.ipynb)** con orquestación del pipeline.

Archivo con historial SQL **[sql_history.sql](sql_history.sql)** de cambios a los datos (en desuso).



## 1. Extraer datos desde .xml y cargarlos a una tabla postgreSQL
### Archivos Extracción /[extraer_desde_Xml](extraer_desde_xml)
Usado paquete `xml.etree.ElementTree` para *parsear* el archivo .xml generado desde Endnote
### Archivos carga a DB /[Carga a postgreSQL](carga_posgres)
Se empleó psql, y el módulo de python **psycopg2**.

## 2. Crear app para buscar por título los DOI que faltan (API de crossref) e insertarlos en su respectiva columna de la tabla.
Uso de API de [CrossRef](https://search.crossref.org/), con librerias de python. Pruebas con:

Probado y descartado:

    pip install crossrefapi

Empleado al final [pag](https://pypi.org/project/habanero/)

    pip install habanero

## 3. Crear app para reinsertar todos los registros en una nueva biblioteca de Endnote

- Prueba generando archivos `.enw`
- Prueba editando el archivo `.xml`, agregando las etiquetas correspondientes al doi (`electronic-resource-num`)  donde sean necesarias.
```
    <electronic-resource-num>
        <style face="normal" font="default" size="100%">...</style>
    </electronic-resource-num>
```