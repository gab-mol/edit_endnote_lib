'''
Pipeline: EndNote Lib. >> .xml >> postgreSQL >> (EDIT) >> EndNote Lib.

'''
import sys
import os
import io 

from extraer_desde_xml.extrac_xml_to_df import extr_opc2
import carga_posgres.load as db
from completar_doi.add_doi import buscar_doi_v0
import temporizador as temp

# Cambiar la codificación de la salida estándar a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

print(f"--- INICIO: {temp.timestamp()} ---")
tiempo = temp.TiempoEjec()

# switch(s) ejec.
ejecutar_extrac_xml = False
ejecutar_carga_sql = False
busqueda_doi_journ = False

# Extraction desde .xml | DONE
if ejecutar_extrac_xml:
    df = extr_opc2('extraer_desde_xml\Endnote 20-10-22.xml')
    print(df.head(10))

# Carga a postgreSQL | DONE
if ejecutar_carga_sql:
    db.tabla_referencias()
    db.load_all(df, True)

## NOTA: en W psql no está bien configurado para mostrar la codificación de los registros

# Completar DOIs faltantes

## SOLO para 'Journal Article' DONE
if busqueda_doi_journ:
    resp = db.query_sql('''
        select nregistro, titulo from endnote.referencias 
            where 
                año > 2000 and
                doi is null and
                tipo = 'Journal Article';
    ''', cerrar = False)

    df_sindoi = db.registros_a_df(resp, ["nregistro", "titulo"])

    titulos = list(df_sindoi['titulo'])

    def map_doi(tit):
        res = buscar_doi_v0(
            titulo = tit, 
            nitems = 10,
            terminal= True
        )
        return res['DOI'] if res else 'no hallado'

    dois = list(map(lambda t: map_doi(t), titulos))
    df_sindoi.insert(2, "doi_nuevo", dois)

    db.query_sql('''
        create table if not exists endnote.busqueda_doi (
            nregistro INTEGER NOT NULL PRIMARY KEY,        
            titulo VARCHAR(440),
            doi_nuevo VARCHAR(125)
            );''', 
            cerrar = False
    )

    # INSERTAR en tabla "busqueda_doi"

    db.load_to(df_sindoi, db.ESQUEMA, "busqueda_doi")

    # Pasar a tabla "referencias" los DOI descargados
    db.query_sql('''
            UPDATE endnote.referencias r
            SET doi = bd.doi_nuevo
            from   (select nregistro, doi_nuevo
                    from endnote.busqueda_doi
                    where doi_nuevo != 'no hallado') as bd
            where 
                    bd.nregistro = r.nregistro;''', 
            cerrar = False
    )

# Generar archivos .
query_pr = '''
    SELECT 
        tipo, titulo, autores, 
        revista_full, volumen, 
        páginas, año, editorial, 
        titl_sec, doi, ciudad
    FROM endnote.referencias
    WHERE nregistro = 2958;
'''

query = '''
    SELECT 
        tipo, titulo, autores, 
        revista_full, volumen, 
        páginas, año, editorial, 
        titl_sec, doi, ciudad, nregistro
    FROM endnote.referencias
    WHERE tipo = 'Journal Article';
'''

DIR = "actualizar_en\journals"

ref = db.query_sql(query)
for i in range(len(ref)):
    tip = ref[i][0]
    tit = ref[i][1]
    auts = ref[i][2].split(";")
    rev = ref[i][3]
    vol = ref[i][4]
    pag = ref[i][5]
    ano = ref[i][6]
    edi = ref[i][7]
    tit_s = ref[i][8]
    doi = ref[i][9]
    ciu = ref[i][10]

    # id-bd
    nre = ref[i][11]

    file = f"jor_{nre}"
    os.makedirs(DIR, exist_ok=True)

    temp.sleep(1)
    with open(f"{DIR}\{file}.enw", "w", encoding='utf-8') as file:
        file.write(f"%0 {tip}\n")
        file.write(f"%T {tit}\n")
        for a in auts:
            if a[0] == " ": a = a[1:] # falla si es un espacio solo
            file.write(f"%A {a}\n")
        file.write(f"%J {rev}\n") if rev else ""
        file.write(f"%V {vol}\n") if vol else ""
        file.write(f"%P {pag}\n") if pag else ""
        file.write(f"%D {ano}\n") if ano else ""
        file.write(f"%I {edi}, {ciu}\n") if edi else ""
        file.write(f"%B {tit_s}\n") if tit_s else ""
        file.write(f"%R {doi}\n") if doi else ""


print(f"--- TERMINADO EN {round(tiempo.stop(), 3)}s ---")

