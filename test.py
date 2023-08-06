import psycopg2

try:
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='Bantypg', port=5432)
    print("Success")

    cur = conn.cursor()

except Exception as er:
    print(er)