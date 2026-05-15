import os
from dotenv import load_dotenv

load_dotenv()

class Configuraciones:
    __db = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "name": os.getenv("DB_NAME", "chat_rag"),
        "schema": os.getenv("DB_SCHEMA", "public"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres")
    }

    __auth = {
        "salt": os.getenv("AUTH_SALT", "chat_rag_seguro_2026")
    }

    __user_test = {
        "username": os.getenv("TEST_USER_USERNAME", "usuario_prueba"),
        "password": os.getenv("TEST_USER_PASSWORD", "clave123")
    }

    @property
    def db(self) -> dict:
        return self.__db

    @property
    def auth(self) -> dict:
        return self.__auth

    @property
    def user_test(self) -> dict:
        return self.__user_test

config = Configuraciones()
