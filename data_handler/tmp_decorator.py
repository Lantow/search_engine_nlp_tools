def db_connector(func):
    def with_connection_(*args, **kwargs):
        conn_str = f"dbname='django' password='{getenv('DJANGO_PASSWORD')}' " + \
                    f"host='{getenv('DJANGO_HOST')}' user='{getenv('DJANGO_USER')}'"
        conn = psycopg2.connect(conn_str)
        try:
            rv = func(conn, *args, **kwargs)
        except Exception as E:
            conn.rollback()
            print(E)
            logging.error(E)
            raise
        else:
            conn.commit()
        finally:
            conn.close()  
          
        return rv

    return with_connection_