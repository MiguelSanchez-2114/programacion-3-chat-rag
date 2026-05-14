from psycopg2 import connect
from chat_rag.config import config
import os

class BaseDeDatos:
    __instancia = None
    isConectada = False
    db_name = None
    schema = None
    
    @staticmethod
    def instancia():
        if BaseDeDatos.__instancia is None:
            BaseDeDatos.__instancia = BaseDeDatos()
            BaseDeDatos.__instancia.__iniciar_base()
        return BaseDeDatos.__instancia
    
    def __iniciar_base(self):
        conn = self.conectar()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = f"{current_dir}/{self.db_name}.sql"
        print(f"Ejecutando script SQL desde: {path}")
        if conn is not None:
            cursor = conn.cursor()
            with open(path, "r") as f:
                sql = f.read()
                cursor.execute(sql)
                conn.commit()
                print("Base de datos inicializada correctamente.")
        else:
            print("No se pudo conectar a la base de datos para inicializarla.")

    def conectar(self):
        if self.isConectada:
            return self.__instancia.conn
        try:
            self.conn = connect(
                host=config.db['host'],
                database=config.db['name'],
                user=config.db['user'],
                password=config.db['password'],
                port=config.db['port']
            )
            self.isConectada = True
            self.db_name = config.db['name']
            self.schema = config.db['schema']
            return self.conn
        except Exception as e:
            print("Error al conectar a la base de datos:", e)
            self.isConectada = False
            return None

    def desconectar(self) -> bool:
        self.conn.close()
        self.isConectada = False
        return True
