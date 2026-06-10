import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="transportadora",
        user="postgres",
        password="123456"
    )