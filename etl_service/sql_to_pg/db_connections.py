import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from logger import logger
from psycopg2.extras import DictCursor

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
}


def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'db.sqlite')


@contextmanager
def open_sqlite_connection(file_name: str = get_db_path()):
    conn = sqlite3.connect(file_name)
    conn.row_factory = sqlite3.Row
    try:
        logger.info('Creating SQLite connection')
        yield conn.cursor()
    finally:
        logger.info('Closing SQLite connection')
        conn.commit()
        conn.close()


@contextmanager
def open_postgres_connection():
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        logger.info('Creating Postgres connection')
        yield pg_conn.cursor()
    finally:
        logger.info('Closing Postgres connection')
        pg_conn.commit()
        pg_conn.close()
