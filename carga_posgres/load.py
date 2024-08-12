'''
Cargar datos extraídos desde .xml a base de datos postgreSQL local.

'''
import psycopg2 as db

import pandas as pd

def connec():
    '''Conexión con base de datos de referencias.'''
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

# cur = conn.cursor()

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
            autores VARCHAR(3228),
            año VARCHAR(154),
            ciudad VARCHAR(199),
            doi VARCHAR(125),
            editores VARCHAR(139),
            editorial VARCHAR(139),
            numero VARCHAR(14),
            páginas VARCHAR(33),
            revis_ab1 VARCHAR(68),
            revis_ab2 VARCHAR(61),
            revista_full VARCHAR(120),
            tipo VARCHAR(24),
            titl_sec VARCHAR(178),
            titulo VARCHAR(440),
            url VARCHAR(232),
            volumen VARCHAR(47)
        );'''
    )
    conn.commit()
    print(f"COMMIT >CREATE TABLE IF NOT EXISTS {ESQUEMA}.{TABLA}<")

# CARGA

def load_all(conn, df:pd.DataFrame, ver_q=False):
    cur = conn.cursor()
    data = list()

    for i, fila in df.iterrows():
        # print("fila n:°",i)
        data.append(fila)

    args_str = ','.join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    x).decode('utf-8') for x in data)

    # Consulta de inserción
    query = f"INSERT INTO {ESQUEMA}.{TABLA} VALUES " + args_str
    if ver_q:print(query)

    # Ejecutar la consulta
    cur.execute(query)
    conn.commit()

def load_to(conn, df:pd.DataFrame,esquema:str, tabla:str, ver_q=False):
    cur = conn.cursor()
    data = list()

    for i, fila in df.iterrows():
        # print("fila n:°",i)
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
    :cerrar: `bool` cierra conexión por defecto

    ### return 
    `list[tuple]` (cada una es un registro/fila)

    '''
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    
    try:
        resp = cur.fetchall()
        return resp
    except:
        print("!!!  no results to fetch")
        resp = None
    
    if cerrar: conn.close()    

    return resp


def colnames(esquema:str, tabla:str):
    res = query_sql(f'''SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{esquema}'
        AND table_name = '{tabla}'
        ORDER BY ordinal_position;''', False)
    
    return [c[0] for c in res]

def registros_a_df(registros:list[tuple], cols:list[str]) -> pd.DataFrame:

    data = dict()

    for c in cols:
        data[c] = list()

    for i in range(len(registros)):
        for j in range(len(cols)):
            data[cols[j]].append(registros[i][j])

    return pd.DataFrame(data)



if __name__ == "__main__":

    query_sql(connec(),'''
        create table if not exists endnote.busq_doi_todo (
            nregistro INTEGER NOT NULL PRIMARY KEY,        
            titulo VARCHAR(440),
            doi_nuevo VARCHAR(125)
            );''', 
            cerrar = False
    )