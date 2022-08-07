from array import array
import pandas as pd
from pathlib import Path
from typing import List, Optional #para un control de los tipos de datos


def data_processing(list_files:Optional[List[Path]]) -> None:
    """ realizo la normalizacion de los datos y armo un unico dataFrame

    Args:
        list_files (Optional[List[Path]]): la funcion recibe como parametro una lista con las rutas de los archivos CSV fuentes
    """

    # realizo la normalizacion de los datos y armo un unico dataFrame
    # Normalizar toda la información de Museos, Salas de Cine y Bibliotecas
    # Populares, para crear una única tabla.
    # Se incluye una columna con la fuente de datos. 
    
    unique_data = normalize_data(list_files)

    # guardo los resultados en una planilla Excel ---------------------------------------------
    url_result = Path.cwd()
    result = Path(url_result/'resultados.xlsx')
    try:
        writer = pd.ExcelWriter(result, engine="openpyxl", mode='a')
    except:
        writer = pd.ExcelWriter(result, engine="openpyxl")

    unique_data.to_excel(writer, 'resultados')
    # ---Al ejecutar save() si la hoja de Excel esta abierta da Error---
    try:
        writer.save()
        print("Planilla Excel grabada exitosamente")
    except:
        print("La planilla Excel esta abierta y debe estar cerrada \n")
    #--------------------------------------------------------------------------------------------

    # genero la tabla con informacio
    # Procesar los datos conjuntos para poder generar una tabla con la siguiente
    # información:
    #   o Cantidad de registros totales por categoría
    #   o Cantidad de registros totales por fuente
    #   o Cantidad de registros por provincia y categoría
    
    # resultados del procesamiento de cines
    #  Procesar la información de cines para poder crear una tabla que contenga:
    #   o Provincia
    #   o Cantidad de pantallas
    #   o Cantidad de butacas
    #   o Cantidad de espacios INCAA
        

def normalize_data(list_files:Optional[List[Path]]) -> pd.DataFrame:
    # inicializo el array con dataFrame normalizados
    data_frame = []
    for data in list_files:
        # obtengo la categoria
        source = data.stem.split('-', 1)[0]
        if (source == 'museos'):
            df = pd.read_csv(data, sep= ',', encoding="utf-8")
            data = df.drop(['Unnamed: 0',
                            'Observaciones',
                            'subcategoria',
                            'piso',
                            'cod_area',
                            'Latitud',
                            'Longitud',
                            'TipoLatitudLongitud',
                            'Info_adicional',               
                            'fuente',
                            'jurisdiccion',
                            'aÃ±o_inauguracion',
                            'actualizacion'], axis=1)

            data.rename(columns= {  'Cod_Loc': 'cod_localidad',
                                    'IdProvincia': 'id_provincia',
                                    'IdDepartamento': 'id_departamento',
                                    'categoria': 'categoria',
                                    'provincia': 'provincia',
                                    'localidad': 'localidad',
                                    'nombre': 'nombre',
                                    'direccion': 'domicilio',
                                    'CP': 'codigo_postal',
                                    'telefono': 'telefono',
                                    'Mail': 'mail',
                                    'Web': 'web'}, inplace=True)

            data['fuente'] = 'museos'
            data_frame.append(data)

        elif (source == 'cines'):
            df = pd.read_csv(data, sep= ',', encoding="utf-8")
            data = df.drop(['Unnamed: 0',
                            'Observaciones',
                            'Departamento',
                            'Piso',
                            'cod_area',
                            'InformaciÃ³n adicional',
                            'Latitud',
                            'Longitud',                 
                            'TipoLatitudLongitud',
                            'Fuente',
                            'tipo_gestion',
                            'Pantallas',
                            'Butacas',
                            'espacio_INCAA',
                            'aÃ±o_actualizacion'], axis=1)

            data.rename(columns= {  'Cod_Loc': 'cod_localidad',
                                    'IdProvincia': 'id_provincia',
                                    'IdDepartamento': 'id_departamento',
                                    'CategorÃ­a': 'categoria',
                                    'Provincia': 'provincia',
                                    'Localidad': 'localidad',
                                    'Nombre': 'nombre',
                                    'DirecciÃ³n': 'domicilio',
                                    'CP': 'codigo_postal',
                                    'TelÃ©fono': 'telefono',
                                    'Mail': 'mail',
                                    'Web': 'web'}, inplace=True)
            data['fuente'] = 'cines'
            data_frame.append(data)
        else:
            df = pd.read_csv(data, sep= ',', encoding="utf-8")
            data = df.drop(['Unnamed: 0',
                            'Observacion',             
                            'Subcategoria',
                            'Departamento',
                            'Piso',
                            'Cod_tel',
                            'InformaciÃ³n adicional',
                            'Latitud',
                            'Longitud',          
                            'TipoLatitudLongitud',
                            'Fuente',
                            'Tipo_gestion',
                            'aÃ±o_inicio',
                            'AÃ±o_actualizacion'], axis=1)

            data.rename(columns= {  'Cod_Loc': 'cod_localidad',
                                    'IdProvincia': 'id_provincia',
                                    'IdDepartamento': 'id_departamento',
                                    'CategorÃ­a': 'categoria',
                                    'Provincia': 'provincia',
                                    'Localidad': 'localidad',
                                    'Nombre': 'nombre',
                                    'Domicilio': 'domicilio',
                                    'CP': 'codigo_postal',
                                    'TelÃ©fono': 'telefono',
                                    'Mail': 'mail',
                                    'Web': 'web'}, inplace=True)
            data['fuente'] = 'bibliotecas'
            data_frame.append(data)
    normalized_data = pd.concat(data_frame,
                                axis=0,
                                join="outer",
                                ignore_index=False,
                                keys=None,
                                levels=None,
                                names=None,
                                verify_integrity=False,
                                copy=True,

    )
    return normalized_data

