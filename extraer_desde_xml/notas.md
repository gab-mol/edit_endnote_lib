# Extracción desde .xml
### 

    <xml>
        <records
            ... n *  (  <record>...</record> )
        </records>
    </xml>

### etiquetas dentro de `record`:
-  rec-number () 
-  foreign-keys () 
-  number () 
-  database () 
-  source-app () 
-  dates () 
-  style () 
-  volume () 
-  titles () 
-  contributors ( authors ( author ( style ) ) ) 
-  key () 
-  authors () 
-  urls () 
-  ref-type () 
-  year () 
-  title () 
-  pages () 
-  record () 
-  secondary-title () 
-  author () 
-  electronic-resource-num ()

---



### IMPORTANTE 
**psycopg2 trae problemas en la instalación**. Por eso se instaló la alternativa precompilada *psycopg2-binary*

    pip install psycopg2-binary

Se importa como `import psycopg2` de igual modo.


### Columnas quedaron como:

    ['nregistro', 
    'autores', 
    'año', 
    'ciudad', 
    'doi', 
    'editores', 
    'editorial', 
    'numero', 
    'páginas', 
    'revis_ab1', 
    'revis_ab2', 
    'revista_full', 
    'tipo', 
    'titl_sec', 
    'titulo', 
    'url', 
    'volumen']


largos máximos caracteres:

nregistro          4
autores         3228
año              154
ciudad           199
doi              125
editores         139
editorial        139
numero            14
páginas           33
revis_ab1         68
páginas           33
revis_ab1         68
revis_ab2         61
revista_full     120
tipo              24
titl_sec         178
titulo           440
url              232
volumen           47