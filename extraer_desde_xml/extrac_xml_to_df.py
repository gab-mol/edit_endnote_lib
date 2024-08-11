import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import pandas as pd
from pprint import pprint
from xml.dom import minidom


# Extracción
def extr_opc1(root):
    '''Para practicar usando la impresión por terminal y pprint'''
    registros = list()
    for item in root.iter('record'):
        registro = dict()

        # nregistro
        registro["nregistro"] = item.find(".//rec-number").text

        # tipo
        tipo = item.find(".//ref-type")
        registro["tipo"] = tipo.attrib.get('name') if (
            isinstance(tipo, Element)) else None
        
        # autores
        autores = item.find(".//contributors/authors")
        if isinstance(autores, Element):
            registro["autores"] = "; ".join(
                [autor.find("style").text for autor in autores]
            )
        else:
            registro["autores"] = None
        
        # editores
        editores = item.find(".//contributors/secondary-authors")
        if isinstance(editores, Element):
            registro["editores"] = "; ".join(
                [edit.find("style").text for edit in editores]
            )
        else:
            registro["editores"] = None

        # ciudad
        ciudad = item.find(".//pub-location/style")
        registro["ciudad"] = ciudad.text if (
            isinstance(ciudad, Element)) else None
        
        # editorial
        editorial = item.find(".//publisher/style")
        registro["editorial"] = editorial.text if (
            isinstance(editorial, Element)) else None

        # año
        ano = item.find(".//dates/year/style")
        registro["año"] = ano.text if (
            isinstance(ano, Element)) else None
        
        # titulo
        titulos = item.findall(".//titles/title/style")
        if titulos:
            if len(titulos) > 1:
                titulo_l = [t.text for t in titulos]
                
                registro["titulo"] = "".join(
                    [t for t in titulo_l if t is not None])
            else:
                registro["titulo"] = titulos[0].text
        else:
            registro["titulo"] = None
        
        # título libro (book section)
        titls = item.findall(".//titles/secondary-title/style")
        if titls:
            if len(titls) > 1:
                titls_l = [t.text for t in titls]
                
                registro["titl_sec"] = "".join(
                    [t for t in titls_l if t is not None])
            else:
                registro["titl_sec"] = titls[0].text
        else:
            registro["titl_sec"] = None

        # revista
        revis_full = item.find(".//periodical/full-title/style")
        registro["revista_full"] = revis_full.text if (
            isinstance(revis_full, Element)) else None
        
        revis_ab1 = item.find(".//periodical/abbr-1/style")
        registro["revis_ab1"] = revis_ab1.text if (
            isinstance(revis_ab1, Element)) else None
        
        revis_ab2 = item.find(".//periodical/abbr-2/style")
        registro["revis_ab2"] = revis_ab2.text if (
            isinstance(revis_ab2, Element)) else None
        
        # volumen
        volumen = item.find(".//volume/style")
        registro["volumen"] = volumen.text if (
            isinstance(volumen, Element)) else None

        # numero
        numero = item.find(".//number/style")
        registro["numero"] = numero.text if (
            isinstance(numero, Element)) else None

        # páginas
        pags = item.find(".//pages/style")
        registro["páginas"] = pags.text if (
            isinstance(pags, Element)) else None

        # url
        url = item.find(".//urls/related-urls/url/style")
        registro["url"] = url.text if (
            isinstance(url, Element)) else None
        
        # doi
        doi = item.find(".//electronic-resource-num/style")
        registro["doi"] = doi.text if (
            isinstance(doi, Element)) else None
        
        # > AGREGAR Registro a lista
        registros.append(registro)

    # print(registros)
    pprint([x for x in registros])
    print("n° registros:",len(registros))

def extr_opc2(path:str) -> pd.DataFrame:
    '''Extracción y conversión a pandas.Dataframe.
    
    ### Parámetro
        :path: ruta al archivo .xml
    '''

    # Carga de archivo .xml
    root = ET.parse(path)

    registros = {
        'nregistro': list(),        
        'autores': list(),
        'año': list(),
        'ciudad': list(),
        'doi': list(),
        'editores': list(),
        'editorial': list(),
        'numero': list(),
        'páginas': list(),
        'revis_ab1': list(),
        'revis_ab2': list(),
        'revista_full': list(),
        'tipo': list(),
        'titl_sec': list(),
        'titulo': list(),
        'url': list(),
        'volumen': list(),
    }
    
    for item in root.iter('record'):

        # nregistro
        registros["nregistro"].append(item.find(".//rec-number").text) 

        # tipo
        tipo = item.find(".//ref-type")
        registros["tipo"].append(tipo.attrib.get('name') if (
            isinstance(tipo, Element)) else None)
        
        # autores
        autores = item.find(".//contributors/authors")
        if isinstance(autores, Element):
            registros["autores"].append("; ".join(
                [autor.find("style").text for autor in autores]
            ))
        else:
            registros["autores"].append(None)
        
        # editores
        editores = item.find(".//contributors/secondary-authors")
        if isinstance(editores, Element):
            registros["editores"].append("; ".join(
                [edit.find("style").text for edit in editores]
            ))
        else:
            registros["editores"].append(None)

        # ciudad
        ciudad = item.find(".//pub-location/style")
        registros["ciudad"].append(ciudad.text if (
            isinstance(ciudad, Element)) else None)
        
        # editorial
        editorial = item.find(".//publisher/style")
        registros["editorial"].append(editorial.text if (
            isinstance(editorial, Element)) else None)

        # año
        ano = item.find(".//dates/year/style")
        registros["año"].append(ano.text if (
            isinstance(ano, Element)) else None)
        
        # titulo
        titulos = item.findall(".//titles/title/style")
        if titulos:
            if len(titulos) > 1:
                titulo_l = [t.text for t in titulos]
                
                registros["titulo"].append("".join(
                    [t for t in titulo_l if t is not None]))
            else:
                registros["titulo"].append(titulos[0].text)
        else:
            registros["titulo"].append(None)
        
        # título libro (book section)
        titls = item.findall(".//titles/secondary-title/style")
        if titls:
            if len(titls) > 1:
                titls_l = [t.text for t in titls]
                
                registros["titl_sec"].append("".join(
                    [t for t in titls_l if t is not None]))
            else:
                registros["titl_sec"].append(titls[0].text)
        else:
            registros["titl_sec"].append(None)

        # revista
        revis_full = item.find(".//periodical/full-title/style")
        registros["revista_full"].append(revis_full.text if (
            isinstance(revis_full, Element)) else None)
        
        revis_ab1 = item.find(".//periodical/abbr-1/style")
        registros["revis_ab1"].append(revis_ab1.text if (
            isinstance(revis_ab1, Element)) else None)
        
        revis_ab2 = item.find(".//periodical/abbr-2/style")
        registros["revis_ab2"].append(revis_ab2.text if (
            isinstance(revis_ab2, Element)) else None)
        
        # volumen
        volumen = item.find(".//volume/style")
        registros["volumen"].append(volumen.text if (
            isinstance(volumen, Element)) else None)

        # numero
        numero = item.find(".//number/style")
        registros["numero"].append(numero.text if (
            isinstance(numero, Element)) else None)

        # páginas
        pags = item.find(".//pages/style")
        registros["páginas"].append(pags.text if (
            isinstance(pags, Element)) else None)

        # url
        url = item.find(".//urls/related-urls/url/style")
        registros["url"].append(url.text if (
            isinstance(url, Element)) else None)
        
        # doi
        doi = item.find(".//electronic-resource-num/style")
        registros["doi"].append(doi.text if (
            isinstance(doi, Element)) else None)

    return pd.DataFrame(registros) 

def transf(df):
    '''casteo de columnas.'''
    colsaint = ['nregistro',
                'año']
    
    colsastr = [
            'autores', 
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
            'volumen'
            ]
    
    # a int
    for c in colsaint:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    # a str
    for c in colsastr:
        df[c] = df[c].astype(str)
    
    print(df)
    return df

def largos(df):
    max_lengths = df.apply(
        lambda col: col.astype(str).apply(len).max())
    print(max_lengths)

def xml_doi(path:str):
    '''
    Agregar la etiqueta correspondiente al doi* a los
    registros que lo requieren en
    ".//record/electronic-resource-num/style":

    `<electronic-resource-num>`  
    `   <style face="normal" font="default" size="100%">*</style>`  
    `</electronic-resource-num>`  
    '''
    tree = ET.parse(path)
    root = tree.getroot()

    # Cargar el archivo XML
    tree = ET.parse(path)
    root = tree.getroot()

    # Iterar sobre todos los elementos <book> en el XML
    for book in root.findall('.//book'):
        # Verificar si el elemento <isbn> existe
        isbn = book.find('isbn')
        
        if isbn is None:
            # Si no existe, agregar la etiqueta <isbn> con un valor predeterminado
            new_isbn = ET.Element('isbn')
            new_isbn.text = 'Sin ISBN'
            book.append(new_isbn)

    # Guardar el archivo XML modificado
    tree.write('extraer_desde_xml/mod_pr.xml', encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":

    # PRUEBAS MANIPIULACIÓN DE ARCHIVOS XML

    tree = ET.parse("extraer_desde_xml/mod_pr.xml")
    root = tree.getroot()

    for b in root.findall('.//book'):
        print(b.find('title').text)
        isbn = b.find('isbn')
        if isbn is not None:
            print("\t",isbn.text)
            isbn.set("atr_n0","valor atrn00")
            isbn.set("atr_n1","valor atrn11")
            isbn.set("atr_n2","valor atrn22")
        else:
            print("\tno isbn")

        xml_str = ET.tostring(root, encoding='utf-8')
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml_str = parsed_xml.toprettyxml(indent="  ")
        with open("extraer_desde_xml/mod_pr2.xml", "w", encoding='utf-8') as f:
            f.write(pretty_xml_str)

    # tree.write('extraer_desde_xml/mod_pr2.xml', encoding='utf-8', xml_declaration=True)

    # # Usar minidom para formatear el XML
    # with open("extraer_desde_xml/Endnote 09-08-24.xml", 'r', encoding='utf-8') as file:
    #     xml_str = file.read()

    # parsed_xml = minidom.parseString(xml_str)
    # formatted_xml = parsed_xml.toprettyxml(indent="  ")

    # # Guardar el XML formateado en el archivo final
    # with open('extraer_desde_xml/Endnote 09-08-24 MOD.xml', 'w', encoding='utf-8') as file:
    #     file.write(formatted_xml)
