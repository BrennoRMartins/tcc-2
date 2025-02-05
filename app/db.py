import psycopg2 as ps
from psycopg2 import OperationalError

def conn():
    try:
        connection = ps.connect(host='localhost', database='tcc', user='postgres', password='123', port="5432")
        print("sucesso")
        return connection
    except OperationalError as e :
        print(f'erro {e}')
