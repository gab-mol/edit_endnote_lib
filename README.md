# Completar Biblioteca de Endnote

La idea de este pequeño proyecto fue encontrar un método automatizado para agregar a los registros de una biblioteca de [EndNote](https://endnote.com/) (EndNote 20 v.: 20.2.1) sus respectivos **DOI** (Digital Object Identifier).

Archivo principal de ejecución: **[main.ipynb](main.ipynb)**. Contiene la orquestación del pipeline y su documentación paso por paso.

## 1. Extraer datos desde .xml y cargarlos a una tabla postgreSQL
### Extracción: /[extraer_desde_Xml](extraer_desde_xml)
Se usó la funcionalidad de exportación de Endnote para transformar toda la biblioteca a `.xml`.

Usado paquete `xml.etree.ElementTree` para *parsear* el archivo .xml generado desde Endnote.

### Carga a DB /[Carga a postgreSQL](carga_posgres)
Se empleó psql, y el módulo de python **psycopg2**.

## 2. Buscar por título los DOI que faltan (API de crossref) e insertarlos en su respectiva columna de la tabla. /[Completar doi](completar_doi)
Uso de API de [CrossRef](https://search.crossref.org/), con librerias de python. Probado y descartado módulo **crossrefapi**. Empleado al final [habanero](https://pypi.org/project/habanero/). Función de búsqueda: `completar_doi.add_doi.buscar_doi_v0`.

Resultados de búsqueda almacenados temporalmente en BD postgreSQL.

## 3. Reinsertar todos los registros en una nueva biblioteca de Endnote
Inicialmente se probó la generación de `.enw` para cada registro (Endnote los usa para insertar registros nuevos). Al final, se recurrió a la edición del archivo `.xml` de exportación, agregando las etiquetas correspondientes al doi (`electronic-resource-num`)  donde fueran necesarias (`xml_doi`)

```
    <electronic-resource-num>
        <style face="normal" font="default" size="100%">...</style>
    </electronic-resource-num>
```
La cadena de texto luego se formateó y guardó como .xml compatible con EndNote.

## 4. Importar a EndNote
Luego se empleó la funcionalidad de importación de Endnote para generar la biblioteca actualizada.