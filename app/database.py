import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="schemenavigator",
        user="postgres",
        password="8951245387",
        host="localhost",
        port="5432"
    )