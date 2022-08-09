import pandas as pd
from sqlalchemy import create_engine
from typing import Optional #para un control de los tipos de datos

def database(data:Optional[pd.DataFrame]) -> None:
    engine = create_engine('postgresql://postgres:1234@localhost:5432/alkemydb')
    #engine = create_engine('mysql+pymysql://root:administrador@localhost/alkemydb')
    data.to_sql(con = engine, name = 'espacios', if_exists='replace')
    print("paso por la base de datos!!!!")
