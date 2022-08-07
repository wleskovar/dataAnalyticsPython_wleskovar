from datetime import date as dt_date
from pathlib import Path
from typing import Optional #para un control de los tipos de datos

ALKEMY = ".alkemy"
MUSEOS = "museos"
CINES = "cines"
BIBLIOTECAS = "bibliotecas"

def make_estructure_dir(url_base:Optional[str] = None) -> Path:
    """ Esta funcion crea el arbol de directorios para almacenar los dataset de trabajo, .alkemy es la raiz de las categorias
        Para no tener que verificar cada vez si la estructura existe, se graba un archivo alkemy.txt como verificador. Si no existe, 
        se generan los directorios, si existe, no se vuelve a genera los directorios.   
        La funcion retorna un objeto Path con la url base, esta se utilizara en la funcion que graba los dataset. 

    Args:
        url_base (Optional[str], optional): puede o no recibir parametros, si lo recibe sera la raiz de donde armar el arbol. Defaults to None.
    """
    url_base = url_base if url_base is not None else Path.cwd()
    
    # A traves de un archivo de control "alkemy.txt" verificamos si la estructura ya fue creada, si esta no fue creada
    # se graba el archivo txt con la fecha en que se creo la estructura.
    file_control = Path(url_base/"alkemy.txt")
    if not file_control.exists():
        file_open =open(file_control, 'w')
        day_create = dt_date.strftime(dt_date.today(), "%Y/%m/%d")
        print(day_create)
        file_open.write(day_create)
        file_open.close()
        
        # chequear si la carpeta existe, si no, la crea
        dataset_path = url_base/ALKEMY/MUSEOS
        if not (Path(dataset_path).exists()):
            Path(dataset_path).mkdir(parents=True)

        dataset_path = url_base/ALKEMY/CINES
        if not (Path(dataset_path).exists()):
            Path(dataset_path).mkdir(parents=True)

        dataset_path = url_base/ALKEMY/BIBLIOTECAS
        if not (Path(dataset_path).exists()):
            Path(dataset_path).mkdir(parents=True)
    else:
        file_open =open(file_control, 'r')
        date_create = file_open.read()
        print("La estructura de directorios ya fue creada el " + date_create )
    
    return Path(url_base/ALKEMY)
    
