import psycopg2
import sys
from functools import wraps
from os import getenv 

conn_str = " ".join(["dbname='django'",
                    f"password='{getenv('DJANGO_PASSWORD')}'", 
                    f"host='{getenv('DJANGO_HOST')}'",
                    f"user='{getenv('DJANGO_USER')}'"])

class PostgresConnection(object):
    """automatic open and close"""    
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None 

    def __enter__(self):
        self.conn = psycopg2.connect(self.conn_str)
        return self    
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


#https://www.psycopg.org/docs/cursor.html#cursor-iterable

def with_conn(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        with PostgresConnection(conn_str) as conn_obj:
            with conn_obj.conn.cursor() as curr:
                return f(*args, conn=conn_obj.conn, curr=curr, **kwds)
    return wrapper

@with_conn
def test_func(exec_str, curr=None, **kwds):
    curr.execute(exec_str)
    t = [c for c in curr]
    print(t[1])

test_func("""SELECT document_text from public.scrapers_retsinfodocument""")
