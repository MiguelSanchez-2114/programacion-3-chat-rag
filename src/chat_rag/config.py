import os
from dotenv import load_dotenv

load_dotenv()

class Configuraciones:
    __env = os.getenv("ENV", "dev")

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

    __file_types_allowed = [t.strip() for t in os.getenv("FILE_TYPES_ALLOWED", ".txt,.pdf").split(",")]
    __file_storage_path = os.path.dirname(os.path.abspath(__file__)) + "/" + os.getenv("FILE_STORAGE_PATH", "uploaded_files/[id_user]/")

    __gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    @property
    def env(self) -> str:
        return self.__env

    @property
    def db(self) -> dict:
        return self.__db

    @property
    def auth(self) -> dict:
        return self.__auth

    @property
    def user_test(self) -> dict:
        return self.__user_test

    @property
    def file_types_allowed(self) -> list:
        return self.__file_types_allowed

    @property
    def file_storage_path(self) -> str:
        return self.__file_storage_path
    
    @property
    def gemini_api_key(self) -> str:
        return self.__gemini_api_key

config = Configuraciones()
