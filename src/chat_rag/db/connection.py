from psycopg import Connection, connect
from chat_rag.config import settings

class BaseDeDatos:
    __instancia = None
    isConectada = False
    
    def instancia(self):
        if self.__instancia is None:
            self.__instancia = BaseDeDatos()
        return self.__instancia

    def conectar(self) -> Connection:
        if self.isConectada:
            return self.__instancia.conn
        self.conn = connect(settings.db_connection_string)
        self.isConectada = True
        return self.conn

    def desconectar(self) -> bool:
        self.conn.close()
        self.isConectada = False
        return True
