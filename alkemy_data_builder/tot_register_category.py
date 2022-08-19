import pandas as pd
from pathlib import Path
from typing import Optional  # para un control de los tipos de datos

import logging

RESULTADOS = "resultados"

# defino una funcion para realizar la tabla de totales de registros por catergori, utilizo pivot_table
def tot_register_category(df: Optional[pd.DataFrame], url_root: Optional[Path]) -> None:
    """Procesar los datos conjuntos para poder generar una tabla con la siguiente información:
            o Cantidad de registros totales por categoría
            o Cantidad de registros totales por fuente
            o Cantidad de registros por provincia y categoría

    Args:
        df (Optional[pd.DataFrame]): Recibe el DataFrame "data", con toda la informacion unificada de las fuentes
        url_root (Optional[Path]): Recibe la raiz del directorio "resultados" en donde guarda el CSV con el reporte.
    """
    logger = logging.getLogger()

    result = pd.pivot_table(
        df,
        index=["id_provincia", "provincia"],
        columns=df.categoria,
        aggfunc="count",
        values="categoria",
    )
    result.loc["Total", :] = result.sum(0).values

    # grabo el archivo CSV con los resultados
    file_csv = "resul_category.csv"
    path_csv = Path(url_root / RESULTADOS / file_csv)
    try:
        result.to_csv(path_csv, sep=",", encoding="latin1")
        # para el logging
        logger.info(
            f"Se grabo un archivo CSV con los datos del reporte solicitado de cantidad de registros"
        )
    except Exception as ex:
        # para el logging
        logger.error(
            f"Error al querer grabar el archivo CSV con los datos del reporte solicitado de cantidad de registros"
        )
        logger.error(ex)
