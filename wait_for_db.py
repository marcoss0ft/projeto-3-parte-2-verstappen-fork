import time
import psycopg2
from psycopg2 import OperationalError

db_ready = False
while not db_ready:
    try:
        conn = psycopg2.connect(
            dbname="f1club2024",
            user="f1club2024user",
            password="f1club2024senha",
            host="db",
            port="5432",
        )
        db_ready = True
    except OperationalError:
        print("Banco de dados não está pronto. Tentando novamente...")
        time.sleep(3)

print("Banco de dados pronto!")