from os import getenv

from dotenv import load_dotenv


load_dotenv()

DB_HOST = getenv('POSTGRES_HOST')
DB_PORT = getenv('POSTGRES_PORT')
DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')
