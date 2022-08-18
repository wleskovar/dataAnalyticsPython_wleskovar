import logging
from decouple import config

import pandas as pd
from datetime import datetime as dt_dt 
from sqlalchemy import create_engine, Integer, String, DateTime
from typing import Optional #para un control de los tipos de datos

def _get_config():
    # Python_decouple
    confi = {'engine': config('ENGINE'),
             'usr': config('USR'),
             'password': config('PASSWORD'),
             'port': config('PORT'),
             'database': config('DATABASE') }
    return confi

def _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE):
    """ Se genera la coneccion a la base de datos correspondiente

    Returns:
        _type_: se retorna la coneccion para operar con la base de datos.
    """
    return create_engine(f'{ENGINE}://{USR}:{PASSWORD}@localhost:{PORT}/{DATABASE}')

def database(df:Optional[pd.DataFrame], confi=None) -> None:
    """ En esta funcion se graban las tablas en la base de datos 'alkemydb' en Postgresql.

    Args:
        df (Optional[pd.DataFrame]): se recibe como parametro el DataFrame normalizado a partir de las 3 fuentes de Museos, Cines y Biblitecas.
    """
    
    # se llama a la funcion like_table para preparar la informacion de las dos tablas a grabar en la base de datos
    tables_dic = like_table(df)
    data = tables_dic.get('espacios')
    data_provincias = tables_dic.get('provincias')
    
    if confi is None:
        confi = _get_config()
    
    ENGINE = confi.get('engine')
    USR = confi.get('usr')
    PASSWORD = confi.get('password')
    PORT = confi.get('port')
    DATABASE = confi.get('database')

    logger = logging.getLogger()
    try:
        # genero un objeto con la coneccion a la base de datos
        engine = _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE)
        logger.info(f"Coneccion exitosa a la base de datos: {DATABASE} por el puerto: {PORT}")
        data.to_sql(    con = engine,
                        name = 'espacios',
                        schema='public',
                        if_exists='replace',
                        index=True,
                        index_label='id',
                        dtype={
	                           "cod_localidad": Integer,
                               "id_provincia": Integer,
                               "id_departamento": Integer,
                               "categoria": String(100),
	                           "localidad": String(200),
	                           "nombre": String(300),
	                           "domicilio": String(300),
	                           "codigo_postal": String(10),
	                           "telefono": String(300),
	                           "mail": String(300),
	                           "web": String(300),
	                           "fecha": DateTime
                        },
                        method='multi'
                    )
        data_provincias.to_sql( con = engine,
                                name = 'provincias',
                                schema='public',
                                if_exists='replace',
                                index=True,
                                index_label='id_provincia',
                                dtype={
	                                   "provincia": String(150),
	                                   "fecha": DateTime
                                },
                                method='multi'
                        )


        # para el logging
        logging.info("Se actualizaron las tablas de espacios y provincias en la base de datos")
    except Exception as ex:
        logger.error(f"La coneccion a la base de datos: {DATABASE}, no se pudo realizar")
        logger.error(ex)
        raise ex
    
    

def like_table(data:Optional[pd.DataFrame]) -> dict:
    """ En esta funcion se separa el DataFreme que se recibe en los datos para la tabla 'espacios' y la tabla 'provincias'
        Tambien se agrega una columna en ambas tablas con la fecha y hora actual para indicar cuando se genero el registro.

    Args:
        data (Optional[pd.DataFrame]): se recibe el DataFrame a separar con la informacion para las tablas.

    Returns:
        dict: se retorna un diccionario que tiene como claves los nombres de las tablas y los DataFreme correspondientes.
    """
    data_provincia = data.filter(items=['id_provincia', 'provincia'], axis=1)
    data_provincia.set_index('id_provincia', inplace=True)
    data_provincia.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=False)
    data_provincia.sort_index(axis=0, ascending=True, inplace=True)
    data.drop(['provincia'], axis=1, inplace=True)
    data['fecha'] = dt_dt.now()
    data_provincia['fecha'] = dt_dt.now()
    tables_dic = {'espacios': data, 'provincias': data_provincia}
    return tables_dic
    
    
    




