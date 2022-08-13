import pandas as pd
from pathlib import Path
from typing import List, Optional #para un control de los tipos de datos

RESULTADOS =  "resultados"

# Procesar los datos conjuntos para poder generar una tabla con la siguiente información:
#   o Cantidad de registros totales por categoría
#   o Cantidad de registros totales por fuente
#   o Cantidad de registros por provincia y categoría

# defino una funcion para realizar la tabla de totales de registros por catergori, utilizo pivot_table
def tot_register_category( df:Optional[pd.DataFrame], url_root:Optional[Path])-> None:
    """_summary_

    Args:
        df (Optional[pd.DataFrame]): _description_
        url_root (Optional[Path]): _description_
    """
    result =pd.pivot_table(df, index= ['id_provincia', 'provincia'], columns= df.categoria, aggfunc= 'count', values= 'categoria')
    result.loc['Total', : ] = result.sum(0).values

    # grabo el archivo CSV con los resultados
    file_csv = "resul_category.csv"
    path_csv = Path(url_root/RESULTADOS/file_csv)
    try:
        result.to_csv(path_csv, sep= ",", encoding="latin1")
    except Exception as ex:
        print(ex)
       