from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine

from alkemy_data_builder.getCSV import getCSV
from alkemy_data_builder.make_estructure_dir import make_estructure_dir
from alkemy_data_builder.save_datasets import save_datasets
from alkemy_data_builder.data_processing import data_processing
from alkemy_data_builder.tot_register_category import tot_register_category
from alkemy_data_builder.info_cines import info_cines
from alkemy_data_builder.database import database
from alkemy_data_builder.logapp import configure_logger

import logging
from decouple import config


PATH_TO_FILE = Path(__file__).parent / "data/scheme_db.sql"


def _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE):
    """Es genera la coneccion a la base de datos

    Args:
        ENGINE (string): motor de base de datos utilizado
        USR (string): usuario de la base de datos
        PASSWORD (string): password del usuario a la base de datos
        PORT (string): numero de puerto donde esta corriendo la base de datos
        DATABASE (string): nombre de la base de datos

    Returns:
        objeto: puntero a la base de datos
    """
    return create_engine(f"{ENGINE}://{USR}:{PASSWORD}@localhost:{PORT}/{DATABASE}")


def _get_config():
    """Levanta los datos de la configuracion de la base de datos desde el archivo ".env"

    Returns:
        dict: retorna un diccionario con todos los valores de la configuracion
    """
    # Python_decouple
    logger = logging.getLogger()
    try:
        confi = {
            "engine": config("ENGINE"),
            "usr": config("USR"),
            "password": config("PASSWORD"),
            "port": config("PORT"),
            "database": config("DATABASE"),
            "url_museos": config("url_museos"),
            "url_cines": config("url_cines"),
            "url_bibliotecas": config("url_bibliotecas"),
            "url_root": config("root"),
        }
    except Exception as ex:
        logger.error(f"Problema con el archivo de configuracion .env")
        logger.error(ex)
        raise ex

    return confi


def init_db(confi: Optional[dict] = None) -> dict:
    """La funcion crea las tablas en la base de datos

    Args:
        confi (dict, optional): puede recibir o no el diccionario de configuracion Defaults to None.

    Raises:
        ex: Puede fallar la conexion a la base de datos
        ex: Puede no leer el archivo.sql con el query para genera las tablas de la bases de datos, o puede tratar generarlas cuando ya existen.
    """
    configure_logger()

    if confi is None:
        confi = _get_config()

    ENGINE = confi.get("engine")
    USR = confi.get("usr")
    PASSWORD = confi.get("password")
    PORT = confi.get("port")
    DATABASE = confi.get("database")

    logger = logging.getLogger()
    try:
        # genero un objeto con la coneccion a la base de datos
        engine = _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE)
        logger.info(
            f"Coneccion exitosa a la base de datos: {DATABASE} por el puerto: {PORT}"
        )
    except Exception as ex:
        logger.error(
            f"La coneccion a la base de datos: {DATABASE}, no se pudo realizar"
        )
        logger.error(ex)
        raise ex

    try:
        with open(PATH_TO_FILE, "r") as file_sql:
            data_sql = file_sql.read()
            logger.warning("Se carga el archivo data_sql")
            engine.execute(data_sql)
            logger.info("Generada las tablas espacios y provincias")
    except Exception as ex:
        logger.error(ex)
        raise ex


def load_data(conf: Optional[dict] = None) -> dict:
    """Se crea el arbol de directorios si estos no existen. Se verifica si existe o no el archivo "alkemy.txt", si existe, ya esta creado el arbol.
        Esta funcion busca la informacion de las fuentes, graba los archivos CSV de museos, cines y bibliotecas y procesa estos archivos
        generando un unico DataFrame, tambien se realizan los reportes solicitados y graba el DataFreme normalizado en las tablas espacios y provincias

    Args:
        conf (dict, optional): Diccionario con las url de las fuentes. Defaults to None.
    """
    configure_logger()

    if conf is None:
        conf = _get_config()

    logger = logging.getLogger()

    logger.info("Ejecutando modulo de carga y procesamiento de la informacion")

    # ------------------------- Archivos fuente --------------------------------------------------------------------------------#
    # url de los archivos CSV con los que se arman los dataset
    url_museos = conf.get("url_museos")
    url_cines = conf.get("url_cines")
    url_bibliotecas = conf.get("url_bibliotecas")
    url_root = conf.get("url_root")

    # llamo a la funcion que prepara el arbol de directorios donde guardar los archivos CSV, esta retorna un objeto Path con la rais de directorios
    url_root = make_estructure_dir(url_root)

    df_museos = getCSV(url_museos)
    df_cines = getCSV(url_cines)
    df_bibliotecas = getCSV(url_bibliotecas)

    # Armo un diccionario con los diferentes datasets obtenidos de la fuente
    dic_datasets = {
        "museos": df_museos,
        "cines": df_cines,
        "bibliotecas": df_bibliotecas,
    }

    files_to_process = save_datasets(dic_datasets, url_root)

    data = data_processing(files_to_process)

    tot_register_category(data, url_root)

    info_cines(df_cines, url_root)

    database(data)
