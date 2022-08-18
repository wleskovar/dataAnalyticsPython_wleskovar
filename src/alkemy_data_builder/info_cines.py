from asyncio.log import logger
import pandas as pd
from pathlib import Path
from typing import List, Optional #para un control de los tipos de datos

import logging

RESULTADOS =  "resultados"

# resultados del procesamiento de cines
    #  Procesar la información de cines para poder crear una tabla que contenga:
    #   o Provincia
    #   o Cantidad de pantallas
    #   o Cantidad de butacas
    #   o Cantidad de espacios INCAA

def info_cines( df:Optional[pd.DataFrame], url_root:Optional[Path])-> None:
    """_summary_

    Args:
        df (Optional[pd.DataFrame]): _description_
        url_root (Optional[Path]): _description_
    """
    logger = logging.getLogger()

    result =pd.pivot_table(df, index= ['IdProvincia', 'Provincia'], aggfunc= {'Pantallas': 'sum', 'Butacas': 'sum', 'espacio_INCAA':'count'},
                             values= ['Pantallas', 'Butacas', 'espacio_INCAA'])
    result.loc['Total', : ] = result.sum(0).values

    # grabo el archivo CSV con los resultados
    file_csv = "resul_cines.csv"
    path_csv = Path(url_root/RESULTADOS/file_csv)
    try:
        result.to_csv(path_csv, sep= ",", encoding="latin1")
        # para el logging
        logger.info(f'Se grabo un archivo CSV con los datos del reporte solicitado de cines')
    except Exception as ex:
        # para el logging
        logger.error(f'Error al grabar un archivo CSV con los datos del reporte solicitado de cines')
        logger.error(ex)
       