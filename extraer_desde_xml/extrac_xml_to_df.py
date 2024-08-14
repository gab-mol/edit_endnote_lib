import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import pandas as pd
from pprint import pprint
import re


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

def xml_doi(path:str, doi_enc:pd.DataFrame) -> str:
    '''
    Agregar la etiqueta correspondiente al doi* a los
    registros que lo requieren en
    ".//record/electronic-resource-num/style":

    `<electronic-resource-num>`  
    `   <style face="normal" font="default" size="100%">*</style>`  
    `</electronic-resource-num>`
    ### parámetros
        :path: `str` ruta a archivo .xml
        :doi_enc: `pandas.DataFrame` con columnas "nregistro" y "doi_nuevo"
    ### return
    Retorna el árbol xml en forma de `str`
    '''
    # Cargar el archivo XML
    tree = ET.parse(path)
    root = tree.getroot()

    record_iter = root.findall('.//record')

    nregistro = doi_enc["nregistro"].to_list()

    for nr in nregistro:
        doi = doi_enc[doi_enc["nregistro"] == nr].iloc[0]["doi_nuevo"]

        for rec in record_iter:
            # match entre rec-number y nregistro
            rec_num = rec.find('rec-number')
            if rec.text and str(nr) == rec_num.text:
                doi_rec = rec.find('electronic-resource-num')
                if doi_rec is None:
                # Si falta <electronic-resource-num>
                    # etiqueta style
                    nuev_sty = ET.Element('style')
                    nuev_sty.set("face","normal")
                    nuev_sty.set("font","default")
                    nuev_sty.set("size","100%")
                    nuev_sty.text = doi

                    # etiqueta electronic-resource-num
                    nuev_ern = ET.Element('electronic-resource-num')

                    # agregar
                    nuev_ern.append(nuev_sty)
                    rec.append(nuev_ern)
                else:
                    doi_style = doi_rec.find('style')
                    doi_style.text = doi

    return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

def elim_indent(xml_str:str) -> str:
    xml_noindent = "".join(xml_str.split("\n"))
    xml_format = re.sub(r'>\s+<', '><', xml_noindent)

    return xml_format

def guardar_xml(xml_str:str, path_salida:str):
    # Guardar el archivo XML modificado
    try:
        # tree.write(path_salida, encoding='utf-8', xml_declaration=True)
        with open(path_salida, "w", encoding="utf-8") as file:
            file.write(xml_str)
        print("GUARDADO:", path_salida)
    except:
        print("Error al guardar!")




if __name__ == "__main__":

    # PRUEBAS MANIPIULACIÓN DE ARCHIVOS XML
    xmlpr ="extraer_desde_xml\pr.xml"
    tree = ET.parse(xmlpr)
    root = tree.getroot()

    dfpr = pd.DataFrame({
        "nregistro":[2892, 2879],
        "doi_nuevo":["10.doidoidoidoidoidoi","10.17957/IJAB/15.1092"]
    })

    xml_doi(xmlpr, dfpr, "extraer_desde_xml\pr_act.xml")

    
    # for b in root.findall('.//record'):
    #     print(b.find('rec-number').text)

