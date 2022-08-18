from distutils.command.config import config
from pathlib import Path
from asyncio.log import logger
from sqlalchemy import create_engine

from alkemy_data_builder.getCSV import getCVS
from alkemy_data_builder.make_estructure_dir import make_estructure_dir
from alkemy_data_builder.save_datasets import save_datasets
from alkemy_data_builder.data_processing import data_processing
from alkemy_data_builder.tot_register_category import tot_register_category
from alkemy_data_builder.info_cines import info_cines
from alkemy_data_builder.database import database
from alkemy_data_builder.logapp import configure_logger

import logging
from decouple import config


PATH_TO_FILE = Path(__file__).parent/'data/scheme_db.sql'

def _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE):
    """ Se genera la coneccion a la base de datos correspondiente

    Returns:
        _type_: se retorna la coneccion para operar con la base de datos.
    """
    return create_engine(f'{ENGINE}://{USR}:{PASSWORD}@localhost:{PORT}/{DATABASE}')

def _get_config():
    # Python_decouple
    confi = {'engine': config('ENGINE'),
             'usr': config('USR'),
             'password': config('PASSWORD'),
             'port': config('PORT'),
             'database': config('DATABASE') }
    return confi

def init_db(confi=None):
    if confi is None:
        confi = _get_config()
    
    ENGINE = confi.get('engine')
    USR = confi.get('usr')
    PASSWORD = confi.get('password')
    PORT = confi.get('port')
    DATABASE = confi.get('database')

    configure_logger()
    logger = logging.getLogger()
    try:
        # genero un objeto con la coneccion a la base de datos
        engine = _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE)
        logger.info(f"Coneccion exitosa a la base de datos: {DATABASE} por el puerto: {PORT}")
    except Exception as ex:
        logger.error(f"La coneccion a la base de datos: {DATABASE}, no se pudo realizar")
        logger.error(ex)
        raise ex

    try:
        with open(PATH_TO_FILE, 'r') as file_sql:
            data_sql = file_sql.read()
            logger.warning("Se carga el archivo data_sql")
            engine.execute(data_sql)
            logger.info('Generada las tablas espacios y provincias')
    except Exception as ex:
        logger.error('Error al abrir el archivo SQL')
        logger.error(ex)
        raise ex
        

def _get_conf_urls():
    # Python_decouple
    conf = {'url_museos': config('url_museos'),
            'url_cines': config('url_cines'),
            'url_bibliotecas': config('url_bibliotecas') }
    return conf

def load_data(conf=None):
    if conf is None:
        conf = _get_conf_urls()

    configure_logger()
    logger = logging.getLogger()

    logger.info('Ejecutando modulo de carga y procesamiento de la informacion')

    #------------------------- Archivos fuente --------------------------------------------------------------------------------#

    # url de los archivos CSV con los que se arman los dataset

    url_museos = conf.get("url_museos")
    url_cines = conf.get("url_cines")
    url_bibliotecas = conf.get("url_bibliotecas")
    
    # llamo a la funcion que prepara el arbol de directorios donde guardar los archivos CSV, esta retorna un objeto Path con la rais de directorios
    url_root = make_estructure_dir()


    df_museos = getCVS(url_museos)
    df_cines = getCVS(url_cines)
    df_bibliotecas = getCVS(url_bibliotecas)

    # Armo un diccionario con los diferentes datasets obtenidos de la fuente
    dic_datasets = {"museos": df_museos, "cines": df_cines, "bibliotecas": df_bibliotecas}

    files_to_process = save_datasets(dic_datasets, url_root)


    #------------------------- Procesamiento de datos -------------------------------------------------------------------------#
    # se genera un DataFrame normalizado a partir de la informacion de las tres fuentes
    data = data_processing(files_to_process)

    # Procesar los datos conjuntos para poder generar una tabla con la siguiente información:
    #   o Cantidad de registros totales por categoría
    #   o Cantidad de registros totales por fuente
    #   o Cantidad de registros por provincia y categoría
    #
    # en el directorio resultados, se guardan los recultados
    tot_register_category(data, url_root)

    # resultados del procesamiento de cines
        #  Procesar la información de cines para poder crear una tabla que contenga:
        #   o Provincia
        #   o Cantidad de pantallas
        #   o Cantidad de butacas
        #   o Cantidad de espacios INCAA
    info_cines(df_cines, url_root)

    #------------------------- Actualizacion de tablas en la Base de datos ---------------------------------------------------------#
    # se actualizan la tablas 'espacios' y 'provincias'
    database(data)


