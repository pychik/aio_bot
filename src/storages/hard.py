import psycopg2
from config import settings


conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER,
                        password=settings.POSTGRES_PASSWORD, host=settings.DB_HOST, port=settings.DB_PORT)
cur = conn.cursor()
