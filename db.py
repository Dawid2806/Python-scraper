import pymysql
import pymysql.cursors




def show_tables():
    try:
        conn = pymysql.connect(**database_config)
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            for table in cursor.fetchall():
                print(table)
        conn.close()
    except Exception as e:
        print(f"Błąd podczas wykonania zapytania: {e}")


def get_db_connection():

    connection = pymysql.connect(
        host=database_config['host'],
        user=database_config['user'],
        password=database_config['password'],
        database=database_config['database'],
        port=database_config['port'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def init_db():
    """
    Inicjalizuje bazę danych, np. tworząc tabelę, jeśli jeszcze nie istnieje.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_url TEXT,
                title TEXT,
                categories TEXT,
                description TEXT
            )
            ''')
        conn.commit()
    finally:
        conn.close()


def execute_query(query, params=None):

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    return result


show_tables()
get_db_connection()
init_db()
