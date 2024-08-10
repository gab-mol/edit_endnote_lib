'''
Revisar que se estén cargando bien los DOIs.
'''

import sys
import io 
import pandas as pd

from extraer_desde_xml.extrac_xml_to_df import extr_opc2
import carga_posgres.load as db
from completar_doi.add_doi import buscar_doi_v0, verificar_doi
import temporizador as temp

# Cambiar la codificación de la salida estándar a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def muestrear(esquema:str, tabla:str, cond_filto=None, porc=0.25, verq=False):
    '''
    Muestrar aleatoriamente un porcentaje de las filas de una tabla.

    ### parámetros

    :esquema: `str` esquema al que pertenece la tabla
    :tabla: `str` nombre de la tabla
    :cond_filto: `str` condición lógica (SQL) opcional para cláusula `WHERE`
    :porc: `float` porcentaje de filas a muestrear
    :verq: `bool` imprimir query en terminal

    ### return
    
    `tuple[tuple(any)]`
    '''
    where = "WHERE "+cond_filto if cond_filto else ""

    query = f'''
            SELECT * 
            FROM {esquema}.{tabla}
            {where}
            ORDER BY RANDOM()
            LIMIT (SELECT COUNT(*) * {porc} FROM {esquema}.{tabla});
    '''
    muestra = db.query_sql(query, False)

    if verq: print(query)

    return muestra

if __name__ == "__main__":

    esq = "endnote"
    tab = "busqueda_doi"

    n_tab = "rev_doi_j"

    def muestro():
        print("MUESTREO...")
        m25 = muestrear(esq, tab, cond_filto="doi_nuevo <> 'no hallado'", verq=True)
        
        df_m25 = db.registros_a_df(m25,db.colnames(esq, tab))

        doi_nuevo = df_m25["doi_nuevo"].to_list()
        tit_busq = list(map(lambda x: verificar_doi(x), doi_nuevo))

        df_m25.insert(2, "crossref_tit", tit_busq)

        print(df_m25,"\n################################")
        df_m25.to_csv("df_m25.csv", index = False)
    
    def carga():

        df_m25 = pd.read_csv("df_m25.csv")
        # print(df_m25)

        try:
            db.query_sql(f'''
                create table if not exists endnote.{n_tab} (
                    nregistro INTEGER NOT NULL PRIMARY KEY,        
                    titulo VARCHAR(440),
                    crossref_tit VARCHAR(440),
                    doi_nuevo VARCHAR(125)
                    );''', 
                    cerrar = False
            )
        except:
            print("Tabla destino ya existe\n")

        db.load_to(df_m25, esq, n_tab, True)

    # muestro()
    # carga()
    '''
    CARGA EXITOSA. BUSQUEDA DE DOI PARA JOURNALS FUNCIONA ACEPTABLEMENTE BIEN-
    '''
