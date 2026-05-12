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
    
    @property
    def db(self) -> dict:
        return self.__db

config = Configuraciones()
