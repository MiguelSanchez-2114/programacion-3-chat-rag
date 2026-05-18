from chat_rag.db.connection import BaseDeDatos
from chat_rag.db.models.model_base import ModelBase

class ArchivoModel(ModelBase):
    __table_name = "archivo"

    def __init__(self, model: dict[str, object] = None):
        self.__id: int = model.get("id", None) if model else None
        self.__nombre: str = model.get("nombre", None) if model else None
        self.__tipo: str = model.get("tipo", None) if model else None
        self.__tamano: str = model.get("tamano", None) if model else None
        self.__id_conversacion: int = model.get("id_conversacion", None) if model else None
        super().__init__(self.__table_name, {
            "id": self.__id,
            "nombre": self.__nombre,
            "tipo": self.__tipo,
            "tamano": self.__tamano,
            "id_conversacion": self.__id_conversacion,
        })

    @staticmethod
    def obtener_todos() -> list["ArchivoModel"]:
        archivos = ModelBase.obtener_todos(ArchivoModel.__table_name)
        return [ArchivoModel(model=archivo) for archivo in archivos]
    
    @staticmethod
    def obtener_por_id_conversacion(id_conversacion: int) -> "ArchivoModel":
        conexion = ModelBase.obtener_conexion()
        schema = BaseDeDatos.instancia().schema
        try:
            sql = f"""
                SELECT a.id, a.nombre, a.tipo, a.tamano, a.id_conversacion
                FROM {schema}.archivo a
                WHERE a.id_conversacion = %s
            """
            cursor = conexion.cursor()
            cursor.execute(sql, (id_conversacion,))
            record = cursor.fetchone()
            archivo = None
            columnas = [desc[0] for desc in cursor.description]
            if record:
                archivo = ArchivoModel(dict(zip(columnas, record)))
            return archivo if archivo else None
        except Exception as e:
            print(f"Error al obtener el archivo: {e}")
            return None

    @property
    def id(self) -> int:
        self.__id = self.model.get("id", None)
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        self.__id = value
        self.model["id"] = value

    @property
    def nombre(self) -> str:
        self.__nombre = self.model.get("nombre", None)
        return self.__nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        self.__nombre = value
        self.model["nombre"] = value

    @property
    def tipo(self) -> str:
        self.__tipo = self.model.get("tipo", None)
        return self.__tipo

    @tipo.setter
    def tipo(self, value: str) -> None:
        self.__tipo = value
        self.model["tipo"] = value

    @property
    def tamano(self) -> str:
        self.__tamano = self.model.get("tamano", None)
        return self.__tamano

    @tamano.setter
    def tamano(self, value: str) -> None:
        self.__tamano = value
        self.model["tamano"] = value
    
    @property
    def id_conversacion(self) -> int:
        self.__id_conversacion = self.model.get("id_conversacion", None)
        return self.__id_conversacion

    @id_conversacion.setter
    def id_conversacion(self, value: int) -> None:
        self.__id_conversacion = value
        self.model["id_conversacion"] = value
