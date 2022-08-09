import requests
import pandas as pd
from io import StringIO
from typing import Optional #para un control de los tipos de datos


def getCVS(url:Optional[str]) -> pd.DataFrame:
    """ obtiene los archivos fuentes desde la URL especificada y retorna un dataFrame de pandas con la informacion
        Se especifia un encoding UTF-8, es diferente al que viene en la fuente.

    Args:
        url (Optional[str]): es un string con la URL de la fuente

    Returns:
        pd.DataFrame: la inforamcion de la fuente es retornada en un dataFrame
    """
    try:
        response = requests.get(url)
        response.encoding = 'UTF-8' # Se cambia el encoding que viene de origen para que tome bien los acentos y otros caracteres
        df = pd.read_csv(StringIO(response.text), encoding="UTF-8", sep=",")
        return df
    except Exception as ex:
        print(ex)