from array import array
from unittest import result
import pandas as pd
from pathlib import Path
from typing import List, Optional #para un control de los tipos de datos



def data_processing(list_files:Optional[List[Path]]) -> pd.DataFrame:
    """ A partir de los datos de las fuentes, se normalizan y se crea una unica tabla.
        
    Args:
        list_files (Optional[List[Path]]): se recibe una lista de los archivso fuentes CSV a unir en una unica tabla

    Returns:
        pd.DataFrame: se retorna la tabla normalizada que se utilizara para popular la base de datos
    """

    # realizo la normalizacion de los datos y armo un unico dataFrame
    # Normalizar toda la información de Museos, Salas de Cine y Bibliotecas Populares, para crear una única tabla.
    
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
            data_frame.append(data)
        else:
            df = pd.read_csv(data, sep= ',', encoding="utf-8")
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
    # limpio los datos de provincia
    final_data = cleaning_provinces( normalized_data)
    return final_data

    
def cleaning_provinces(data:Optional[pd.DataFrame]) -> pd.DataFrame:
    """ A partir observar los datos, se detectaron algunos registros con diferencias en la carga de las provicias y un 
        registro en particular de Salta en donde se asigno la provincia de Neuquen.
        En esta funcion se corrigen esos datos detectados.

    Args:
        data (pd.DataFrame): se recibe el DataFrame que se esta armando con la informacion de todas las fuentes

    Returns:
       pd.DataFreme: se retorna el DataFrame con las correciones realizadas a provincia.
    """
    data.provincia= data.provincia.apply(lambda x: str(x).replace('Tierra del Fuego, Antártida e Islas del Atlántico Sur', 'Tierra del Fuego'))
    data.provincia= data.provincia.apply(lambda x: str(x).replace('Santa Fé', 'Santa Fe'))
    data.provincia= data.provincia.apply(lambda x: str(x).replace('Neuquén ', 'Neuquén'))
    mask = (data.id_provincia == 58) & (data.provincia == 'Salta')
    data.loc[mask, 'id_provincia'] = 66
    data.loc[mask, 'cod_localidad'] = 66028050
    data.loc[mask, 'codigo_postal'] = 'A4400' 
    
    return data         


