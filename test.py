from alkemy_data_builder.getCSV import getCVS
from alkemy_data_builder.make_estructure_dir import make_estructure_dir
from alkemy_data_builder.save_datasets import save_datasets
from alkemy_data_builder.data_processing import data_processing


#------------------------- Archivos fuente --------------------------------------------------------------------------------#

# Estas lineas deben ser incluidas en un archivo de configuracion

# url de los archivos CSV con los que se arman los dataset
url_museos = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv"
url_cines = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv"
url_bibliotecas = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"

# llamo a la funcion que prepara el arbol de directorios donde guardar los archivos CSV, esta retorna un objeto Path con la rais de directorios
url_root = make_estructure_dir()

df_museos = getCVS(url_museos)
df_cines = getCVS(url_cines)
df_bibliotecas = getCVS(url_bibliotecas)

# Armo un diccionario con los diferentes datasets obtenidos de la fuente
dic_datasets = {"museos": df_museos, "cines": df_cines, "bibliotecas": df_bibliotecas}

files_to_process = save_datasets(dic_datasets, url_root)


#------------------------- Procesamiento de datos -------------------------------------------------------------------------#
data_processing(files_to_process)
#------------------------- Creacion de tablas en la Base de datos ---------------------------------------------------------#

#------------------------- Actualizacion de la base de datos ---------------------------------------------------------------#