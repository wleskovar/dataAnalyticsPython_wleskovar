import requests
import pandas as pd
from io import StringIO


def getCVS(url):
    try:
        response = requests.get(url)
        df = pd.read_csv(StringIO(response.text), encoding="utf-8", sep=",")
        return df
    except Exception as ex:
        print(ex)