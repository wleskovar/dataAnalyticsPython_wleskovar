from asyncio.log import logger
from encodings.utf_8 import encode
from importlib.resources import path
from linecache import cache
import pandas as pd
from datetime import date as dt_date
from pathlib import Path
from typing import Optional #para un control de los tipos de datos

import logging

MUSEOS = "museos"
CINES = "cines"
BIBLIOTECAS = "bibliotecas"
MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def save_datasets(dic_datasets:Optional[dict], url_root:Optional[Path]) -> str:
    """ se graban los archivos csv obtenidos desde la fuente de datos
        se oOrganizan los archivos en rutas siguiendo la siguiente estructura:
        “categoría\año-mes\categoria-dia-mes-año.csv”
        por ejemplo: “museos\2021-noviembre\museos-03-11-2021”
        si el archivo existe debe reemplazarse. La fecha de la nomenclatura es la fecha de descarga.

    Args:
        dic_datasets (Optional[dict]): el diccionario que se pasa como parametro contien los dataFrame a grabar como archivo CSV
        url_root (Optional[Path]): este parametro es un objeto Path que contiene la raiz de los directorios

    Returns:
        str: se retorna un array con la lista de los archivos CSV a procesar
    """

    logger = logging.getLogger()

    # array donde se guardan los archivos grabados y a procesar
    files_creates = []

    # obtengo la fecha del dia para incluir en el nombre del archivo csv a grabar
    day_cvs = dt_date.strftime(dt_date.today(), "%d-%m-%Y")
    # obtengo el año y el mes para generar el subdirectorio donde se guardara el archivo csv
    year = day_cvs[6:]
    month = MES[int(day_cvs[3:5])-1]
    url_date = year + '-' + month
        
    # Museos
    # armo el directorio
    url_museos = Path(url_root/MUSEOS/url_date) 
    if not url_museos.exists():
        url_museos.mkdir()
    # armo el nombre del archivo csv
    file_csv = MUSEOS + "-" + day_cvs + ".csv"
    # grabo el archivo
    path_csv = Path(url_museos/file_csv)
    try:
        dic_datasets.get("museos").to_csv(path_csv, sep= ',', encoding="UTF-8")
        files_creates.append(path_csv)
        # para el logging
        logger.info(f'Se grabo el archivo CSV {MUSEOS}')
    except Exception as ex:
        # para el logging
        logger.error(f'Error al querer grabar el archivo CSV {MUSEOS}')
        logger.error(ex)
    
    # Cines
    # armo el directorio
    url_cines = Path(url_root/CINES/url_date) 
    if not url_cines.exists():
        url_cines.mkdir()
    # armo el nombre del archivo csv
    file_csv = CINES + "-" + day_cvs + ".csv"
    # grabo el archivo
    path_csv = Path(url_cines/file_csv)
    try:
        dic_datasets.get("cines").to_csv(path_csv, sep= ',', encoding="UTF-8")
        files_creates.append(path_csv)
        # para el logging
        logger.info(f'Se grabo el archivo CSV {CINES}')
    except Exception as ex:
        # para el logging
        logger.error(f'Error al querer grabar el archivo CSV {CINES}')
        logger.error(ex)
    
    # Bibliotecas
    # armo el directorio
    url_bibliotecas = Path(url_root/BIBLIOTECAS/url_date) 
    if not url_bibliotecas.exists():
        url_bibliotecas.mkdir()
    # armo el nombre del archivo csv
    file_csv = BIBLIOTECAS + "-" + day_cvs + ".csv"
    # grabo el archivo
    path_csv = Path(url_bibliotecas/file_csv)
    try:
        dic_datasets.get("bibliotecas").to_csv(path_csv, sep= ",", encoding="UTF-8")
        files_creates.append(path_csv)
        # para el logging
        logger.info(f'Se grabo el archivo CSV {BIBLIOTECAS}')
    except Exception as ex:
        # para el logging
        logger.error(f'Error al querer grabar el archivo CSV {BIBLIOTECAS}')
        logger.error(ex)
    return files_creates
   