import psycopg2
import sys

#https://www.psycopg.org/docs/cursor.html#cursor-iterable

USER = "morten"
HOST = "188.166.59.45"
DBNAME = "django"
DBPASS = ""


conn = psycopg2.connect(f"dbname='{DBNAME}' user='{USER}'" + 
                            f"host='{HOST}' password='{DBPASS}'")

curr = conn.cursor()

try:
    curr.execute("""SELECT document_text from public.scrapers_retsinfodocument""")
except Exception as E:
    transaction.rollback()
    print(E)

