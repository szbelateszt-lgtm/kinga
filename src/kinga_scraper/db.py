import mysql.connector
from mysql.connector import errorcode
from .config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4',
        use_unicode=True,
    )


def init_schema():
    with open('sql/kinga_schema.sql', 'r', encoding='utf-8') as schema_file:
        schema_sql = schema_file.read()

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        charset='utf8mb4',
        use_unicode=True,
    )
    conn.autocommit = True
    cursor = conn.cursor()
    for statement in schema_sql.split(';'):
        statement = statement.strip()
        if not statement:
            continue
        cursor.execute(statement)
    cursor.close()
    conn.close()
