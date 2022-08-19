# dataAnalyticsPython_wleskovar
Objetivo 👈 Para resolver este challenge, deberás crear un proyecto que consuma datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.

# Dependencias

sqlalchemy>=1.4.39

requests>=2.28.1

openpyxl>=3.0.10

pandas>=1.4.3

psycopg2>=2.9.3

python-decouple>=3.6

python-dotenv>=0.20.0

# Instalacion

Para instalar el paquete:

```bash
pip install git+https://github.com/wleskovar/dataAnalyticsPython_wleskovar.git
```
# Configuracion

En el archivo .env en la raiz del proyecto se deben configurar:

Los parametros de la base de datos.
Las url de donde se encuetran las fuentes.
la raiz desde donde se quieren crear los directoros para contener los archivos CSV de las fuentes bajados de internte. Si se deja el string '.'
los directoros se generan a partir de donde se esta ejecutando el proyecto.

El archivo de configuracion deberia verse de la siguiente manera:

```bash
ENGINE = 'postgresql'
USR = 'postgres'
PASSWORD = '1234'
PORT = '5432'
DATABASE = 'alkemydb'

url_museos = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv"
url_cines = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv"
url_bibliotecas = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"

root = "."
```

# Ejecucion

El programa se puede ejecutar desde la terminal, se puede correr con parametros o sin parametros:

```bash
python -m alkemy_data_buider -h, muestra un help con la informacion de los parametros que acepta.
```

```bash
python -m alkemy_data_builder
```
Al no tener parametros por default ejecuta el scrip "load_data":
    . Obtiene la informacion de internet
    . Genera el arbol de directorios
    . Graba los archivos CSV con la informacion de las fuentes 
    . Procesa los archivos CSV, normalizando la informacion en un unico DataFrame
    . Graba la informacion en las tablas "espacios" y "provincias" en la base de datos
    . Graba las salidas de las consultas solicitadas en el directorio .alkemy/resultados

```bash
python -m alkemy_data_builder -s load_data
```
Ejecuta el scrip "load_data, ver punto anterior.

```bash
python -m alkemy_data_builder -s init_db
```
Ejecuta el scrip "init_db, este script levanta un archivo .sql y genera las tablas "espacios" y "provincias"
en la base de datos definida en el archivo .env. La base de datos debe exisitir, el archivo.sql solo tiene las sentencias para la creacion de
las tablas.

```bash
python -m alkemy_data_builder -s ambos
```
Ejecuta ambos scripts, primero el init_db para generar las tablas y despues load_db que obtiene, procesa y graba toda la informacion.

Alternativamente si que quieren ejecutar las funciones desde otro programa de Python, se deben importar del paquete alkemy_data_builder:
init_db - genera las tablas de la base de datos
load_data - genera la informacion a cargar en la base de datos y los reportes

Ver en la raiz del proyecto un ejemplo en el archivo ejemplo.py
```bash
python ejemplo.py
```


