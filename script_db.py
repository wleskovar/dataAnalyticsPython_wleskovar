from sqlalchemy import create_engine


# defino las credenciales de la base de datos postgreSQL
ENGINE = 'postgresql'
USR = 'postgres'
PASSWORD = '1234'
PORT = '5432'
DATABASE = 'alkemydb'

PATH_TO_FILE = 'C:/Users/wlesk/Documents/DataAnalytics/Alkemy/dataAnalyticsPython_wleskovar/scheme_db.sql'


def get_connection():
    """ Se genera la coneccion a la base de datos correspondiente

    Returns:
        _type_: se retorna la coneccion para operar con la base de datos.
    """
    return create_engine(f'{ENGINE}://{USR}:{PASSWORD}@localhost:{PORT}/{DATABASE}')

if __name__ == '__main__':
    try:
        # genero un objeto con la coneccion a la base de datos
        engine = get_connection()
        print(f"Coneccion exitosa a la base de datos: {DATABASE} por el puerto: {PORT}")
    except Exception as ex:
        print(f"La coneccion a la base de datos: {DATABASE}, no se pudo realizar")

    

    with open(PATH_TO_FILE, 'r') as file_sql:
        try:
            data_sql = file_sql.read()
            print(data_sql)
            engine.execute(data_sql)
            print('generada la tabla')
        except Exception as ex:
            print('error al abrir el archivo SQL')
        




