from array import array
from unittest import result
import pandas as pd
from pathlib import Path
from typing import List, Optional #para un control de los tipos de datos


def data_processing(list_files:Optional[List[Path]]) -> pd.DataFrame:
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
    # url_result = Path.cwd()
    # result = Path(url_result/'resultados.xlsx')
    # try:
    #     writer = pd.ExcelWriter(result, engine="openpyxl", mode='a')
    # except:
    #     writer = pd.ExcelWriter(result, engine="openpyxl")

    # unique_data.to_excel(writer, 'resultados')
    # # ---Al ejecutar save() si la hoja de Excel esta abierta da Error---
    # try:
    #     writer.save()
    #     print("Planilla Excel grabada exitosamente")
    # except:
    #     print("La planilla Excel esta abierta y debe estar cerrada \n")
    #--------------------------------------------------------------------------------------------

    # genero la tabla con informacio
    # Procesar los datos conjuntos para poder generar una tabla con la siguiente
    # información:
    #   o Cantidad de registros totales por categoría
    #   o Cantidad de registros totales por fuente
    #   o Cantidad de registros por provincia y categoría
    results = tot_register_categori(unique_data)

    # resultados del procesamiento de cines
    #  Procesar la información de cines para poder crear una tabla que contenga:
    #   o Provincia
    #   o Cantidad de pantallas
    #   o Cantidad de butacas
    #   o Cantidad de espacios INCAA

    return unique_data
        

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
                            'año_inauguracion',
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
                            'Información adicional',
                            'Latitud',
                            'Longitud',                 
                            'TipoLatitudLongitud',
                            'Fuente',
                            'tipo_gestion',
                            'Pantallas',
                            'Butacas',
                            'espacio_INCAA',
                            'año_actualizacion'], axis=1)

            data.rename(columns= {  'Cod_Loc': 'cod_localidad',
                                    'IdProvincia': 'id_provincia',
                                    'IdDepartamento': 'id_departamento',
                                    'Categoría': 'categoria',
                                    'Provincia': 'provincia',
                                    'Localidad': 'localidad',
                                    'Nombre': 'nombre',
                                    'Dirección': 'domicilio',
                                    'CP': 'codigo_postal',
                                    'Teléfono': 'telefono',
                                    'Mail': 'mail',
                                    'Web': 'web'}, inplace=True)
            data['fuente'] = 'cines'
            data_frame.append(data)
        else:
            df = pd.read_csv(data, sep= ',', encoding="utf-8")
            print(df)
            data = df.drop(['Unnamed: 0',
                            'Observacion',             
                            'Subcategoria',
                            'Departamento',
                            'Piso',
                            'Cod_tel',
                            'Información adicional',
                            'Latitud',
                            'Longitud',          
                            'TipoLatitudLongitud',
                            'Fuente',
                            'Tipo_gestion',
                            'año_inicio',
                            'Año_actualizacion'], axis=1)

            data.rename(columns= {  'Cod_Loc': 'cod_localidad',
                                    'IdProvincia': 'id_provincia',
                                    'IdDepartamento': 'id_departamento',
                                    'Categoría': 'categoria',
                                    'Provincia': 'provincia',
                                    'Localidad': 'localidad',
                                    'Nombre': 'nombre',
                                    'Domicilio': 'domicilio',
                                    'CP': 'codigo_postal',
                                    'Teléfono': 'telefono',
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

# defino una funcion para realizar la tabla de totales de registros por catergori, utilizo pivot_table
def tot_register_categori( data:Optional[pd.DataFrame])-> pd.DataFrame:
    #results = data.pivot_table(index='provincia', columns='categoria', aggfunc='count')

    results = data.categoria.groupby(data.provincia).count()
    results.index.name = 'Categoria'
    
    
    return results
