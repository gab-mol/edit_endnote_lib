from habanero import Crossref
# import pandas as pd

cr = Crossref()


def buscar_doi_v0(titulo:str, nitems=1, siml=.8, terminal=False) -> dict | None:
    '''
    Busca por título y retorna el diccionario de una publicación
    con todos los datos disponibles, solo si se encuentra
    un ítem com % >= `parecido` de coincidencia con el
    título introducido, y si este posee DOI disponible.

    ### parámetros

    :titulo: `str` título de la publicación
    :nitems: `int` número de resultados evaluados
    :siml: `float` porcentaje de similitud umbral del título para 
    aceptar DOI
    :terminal: `bool` imprimir información sobre búsqueda por terminal

    ### return 
        `dict` con datos disponibles | `None`
    '''
    if terminal: print("\n# BUSCAR:", titulo,"#")
    if titulo is None: 
        if terminal:print("!!! Búsqueda abortada.")
        return None
    res = cr.works(query = titulo)
    items = res['message']['items']

    # evitar error si hay pocos resultados
    n = len(items)
    if nitems > n: nitems = n    

    titles = list()

    for i in range(nitems):
        it = items[i]
        keys = list(it.keys())

        if 'title' in keys:
            t = it['title'][0]
            titles.append(t)

    parecido = list()

    # eliminar puntos y mayus del registro, bajan espuriamente la similitud
    tit_s = set(titulo.replace(".", "").lower().split())
    ntit = len(tit_s)
    for t in titles:
        t_s = set(t.lower().split())
        com = len(tit_s.intersection(t_s))
        if len(t_s) > ntit:
            parecido.append(0)
        else:
            parecido.append(com / ntit)
    
    if terminal:
        print("Resultados:")
        for p, t in zip(parecido, titles):
            print(round(p*100,1),"% |", t)

    # Buscar el título más parecido según % de palabras =
    if not any(x >= siml for x in parecido):
        if terminal:
            print("#-RESULTADO--X------X------X------X-#")
            print("Similitud < a", siml*100,"%")
            print("#-----X------X------X------X------X-#")
        return None
    
    if parecido == []: 
        return None

    i = 0
    for p in parecido:
        if p > siml: 
            result = items[i]
            break
        else:
            i += 1
            if i == len(parecido):
                return None
    

    if 'DOI' in result.keys():
        if terminal: 
            print("#-RESULTADO-#########################")
            print(result['title'], "DOI:",result['DOI'])
            print("#####################################")

        return result
    else:
        if terminal: 
            print("El más parecido no tiene DOI disponible:")
            print("tit:",result['title'])
        return None

def verificar_doi(doi:str) -> str:
    '''
    :doi: `str` DOI para realizar búsqueda con Crossref

    :return: título correspondiente al doi introducido.
    '''
    # try:
    res = cr.works(ids=doi)
    # except:
    #     exceptions.HTTPError()
        
    item = res['message']['title']

    return item[0]
  