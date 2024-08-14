# Completar Biblioteca de Endnote

***---EN PROCESO---***

La idea de este pequeño proyecto fue encontrar un método automatizado para agregar a los registros de una biblioteca de [Endnote](https://endnote.com/) sus respectivos **DOI** (Digital Object Identifier).

Archivo principal de ejecución: **[main.ipynb](main.ipynb)**. Contiene la orquestación del pipeline y su documentación paso por paso.

## 1. Extraer datos desde .xml y cargarlos a una tabla postgreSQL
### Archivos Extracción /[extraer_desde_Xml](extraer_desde_xml)
Se usó la funcionalidad de exportación de Endnote para transformar toda la biblioteca a `.xml`.

Usado paquete `xml.etree.ElementTree` para *parsear* el archivo .xml generado desde Endnote.

### Archivos carga a DB /[Carga a postgreSQL](carga_posgres)
Se empleó psql, y el módulo de python **psycopg2**.

## 2. Crear app para buscar por título los DOI que faltan (API de crossref) e insertarlos en su respectiva columna de la tabla.
Uso de API de [CrossRef](https://search.crossref.org/), con librerias de python. Probado y descartado módulo **crossrefapi**. Empleado al final [habanero](https://pypi.org/project/habanero/). Función de búsqueda: `completar_doi.add_doi.buscar_doi_v0`.

Resultados de búsqueda almacenados temporalmente en BD postgreSQL.

## 3. Crear app para reinsertar todos los registros en una nueva biblioteca de Endnote
Inicialmente se probó la generación de `.enw` para cada registro (Endnote los usa para insertar registros nuevos). Al final, se recurrió a la edición del archivo `.xml` de exportación, agregando las etiquetas correspondientes al doi (`electronic-resource-num`)  donde fueran necesarias.

```
    <electronic-resource-num>
        <style face="normal" font="default" size="100%">...</style>
    </electronic-resource-num>
```

Luego se empleó la función de importación para generar la biblioteca 