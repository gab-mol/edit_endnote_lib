'''
Interacción con base de datos postgreSQL local creada para el proyecto.  
(Ver "Carga a base de datos (postgreSQL)" en main.ipynb)
'''
import psycopg2 as db

import pandas as pd

def connec():
    '''Conexión con base de datos del proyecto.'''
    conn = db.connect(
        dbname="endnote_refs",
        user="editor_en",
        password="editarend24",
        host="localhost",
        port="5432"
    )
    return conn

TABLA = "referencias"
ESQUEMA = "endnote"

def tabla_referencias(conn):
    '''
    Crea tabla destino de los datos,
    si esta no existe.

        **Tabla**: 'referencias'  
        **Esquema**: 'endnote'

    '''
    cur = conn.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {ESQUEMA}.{TABLA} ( 
            nregistro INTEGER NOT NULL PRIMARY KEY,        
            autores TEXT,
            año TEXT,
            ciudad TEXT,
            doi TEXT,
            editores TEXT,
            editorial TEXT,
            numero TEXT,
            páginas TEXT,
            revis_ab1 TEXT,
            revis_ab2 TEXT,
            revista_full TEXT,
            tipo TEXT,
            titl_sec TEXT,
            titulo TEXT,
            url TEXT,
            volumen TEXT
        );'''
    )
    conn.commit()
    print(f"COMMIT >CREATE TABLE IF NOT EXISTS {ESQUEMA}.{TABLA}<")

# CARGA

def load_all(conn, df:pd.DataFrame, ver_q=False):
    '''
    Cargar dataframe extraído del archivo XML a base de datos.
    (número de campos establecido para ser compatible con
    tabla generada por `load.tabla_referencias`).

    ### Parámetros
        :conn: objeto de conexión con BD postgres
        :df: `DataFrame` datos extraídos desde archivo de exportación XML
        :ver_q: `bool` imprimir consulta SQL ejecutada
    '''
    cur = conn.cursor()
    data = list()

    for _, fila in df.iterrows():
        data.append(fila)

    args_str = ','.join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    x).decode('utf-8') for x in data)

    # Consulta de inserción
    query = f"INSERT INTO {ESQUEMA}.{TABLA} VALUES " + args_str
    if ver_q:print(query)

    # Ejecutar la consulta
    try:
        cur.execute(query)
        conn.commit()
        print(f"> INSERT INTO {ESQUEMA}.{TABLA} VALUES (<<df>>) <")
    except:
        print(f"> ERROR en commit a {ESQUEMA}.{TABLA} <")

def load_to(conn, df:pd.DataFrame,esquema:str, tabla:str, ver_q=False):
    '''
    Cargar todos los registros de un `pandas.DataFrame` a una tabla de
    postgres preexistente compatible.

    ### Parámetros
        :conn: objeto de conexión con BD postgres
        :df: `DataFrame` datos a insertar
        :esquema: `str` nombre del esquema de la tabla
        :tabla: `str` nombre de la tabla
        :ver_q: `bool` imprimir consulta SQL ejecutada
    '''
    cur = conn.cursor()
    data = list()

    for _, fila in df.iterrows():
        data.append(fila)

    placehold = "("+", ".join(["%s " for _ in range(len(df.columns))])+")"
    args_str = ','.join(
        cur.mogrify(placehold, 
                    x).decode('utf-8') for x in data)

    # Consulta de inserción
    query = f"INSERT INTO {esquema}.{tabla} VALUES " + args_str
    if ver_q:print(query)

    # Ejecutar la consulta
    cur.execute(query)
    conn.commit()

def query_sql(conn, query:str, cerrar=False):
    '''Envoltura de métodos de `psycopg2` para
    ejecución de consultas y retorno de datos.

    ### parámetros

    :query: `str` Consulta en SQL, terminada en `;`
    :cerrar: `bool` cerrar conexión

    ### return 
    `list[tuple]` (cada una es un registro/fila)

    '''
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    try:
        resp = cur.fetchall()
    except:
        print("!!!  no results to fetch")
        resp = None
    
    if cerrar: conn.close()    

    return resp

def colnames(conn, esquema:str, tabla:str) -> list[str]:
    '''
    Obtener nombres de columnas de tabla postgres.

    ### Parámetros
        :conn: objeto de conexión con BD postgres
        :esquema: `str` nombre del esquema de la tabla
        :tabla: `str` nombre de la tabla
    ### return
        `list[str]` de nombres
    '''
    res = query_sql(conn,f'''SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{esquema}'
        AND table_name = '{tabla}'
        ORDER BY ordinal_position;''', False)
    
    return [c[0] for c in res]

def registros_a_df(registros:list[tuple], cols:list[str]) -> pd.DataFrame:
    '''
    Transformar lista de tuplas (=registro) a formato `pandas.DataFrame`.

    ### Parámetros
        :registros: `list[tuple]` datos a transformar
        :cols: `list[str]` nombre de las columnas en el órden correcto
    
    ### return
        Datos formateados como `pandas.DataFrame`.
    '''
    data = dict()

    for c in cols:
        data[c] = list()

    for i in range(len(registros)):
        for j in range(len(cols)):
            data[cols[j]].append(registros[i][j])

    return pd.DataFrame(data)
