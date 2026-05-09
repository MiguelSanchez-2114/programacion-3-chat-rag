from chat_rag.db.connection import BaseDeDatos

class ModelBase():
    __table_name: str
    __model: dict[str, object]
    __db_name: str

    def __init__(self, table_name: str, model: dict[str, object] = None):
        self.__table_name = table_name
        self.__model = model
        self.__db_name = BaseDeDatos.instancia().db_name

    @property
    def table_name(self) -> str:
        return self.__table_name
    
    @property
    def model(self) -> dict[str, object]:
        return self.__model
    
    @staticmethod
    def db_name() -> str:
        return BaseDeDatos.instancia().db_name
    
    @staticmethod
    def __obtener_conexion():
        conexion = BaseDeDatos.instancia().conectar()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            raise Exception("No se pudo establecer conexión a la base de datos.")
        return conexion
    
    @staticmethod
    def obtener_todos(table_name: str) -> list[dict[str, object]]:
        conexion = ModelBase.__obtener_conexion()
        db_name = ModelBase.db_name()
        try:
            sql = f"SELECT * FROM {db_name}.{table_name}"
            cursor = conexion.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return [dict(zip(columnas, record)) for record in records]
        except Exception as e:
            print(f"Error al obtener registros de {table_name}: {e}")
            return []
    
    def __datos_para_guardar(self, omitir_nulos: bool = False) -> dict[str, object]:
        return {key: value for key, value in self.__model.items() if key != "id" and (value is not None or not omitir_nulos)}
    
    def guardar(self):
        if self.model.get("id") is not None:
            print("El registro ya tiene un ID, no se puede guardar como nuevo.")
            return self.actualizar()
        
        conexion = ModelBase.__obtener_conexion()
        try:
            datos = self.__datos_para_guardar(omitir_nulos=True)
            columnas = ", ".join(datos.keys())
            placeholders = ", ".join(["%s"] * len(datos))
            valores = tuple(datos.values())

            sql = f"""
                INSERT INTO {self.__db_name}.{self.table_name} ({columnas})
                VALUES ({placeholders})
                RETURNING id;
            """
            cursor = conexion.cursor()
            cursor.execute(sql, valores)
            nuevo_id = cursor.fetchone()[0]

            print(f"Registro insertado en {self.table_name} con ID: {nuevo_id}")

            conexion.commit()
            
            self.obtener_por_id(nuevo_id)

            return nuevo_id

        except Exception as e:
            conexion.rollback()

            print(f"Error al insertar en {self.table_name}: {e}")
            raise
    
    def actualizar(self):
        conexion = ModelBase.__obtener_conexion()
        try:
            id = self.model.get("id")
            if id is None:
                print("No se puede actualizar un registro sin ID.")
                return False
            datos = self.__datos_para_guardar()
            asignaciones = ", ".join([f"{k} = %s" for k in datos.keys()])
            valores = list(datos.values()) + [id]

            sql = f"""
                UPDATE {self.__db_name}.{self.table_name}
                SET {asignaciones}
                WHERE id = %s
            """

            cursor = conexion.cursor()
            cursor.execute(sql, valores)
            conexion.commit()

            self.obtener_por_id(id)

            return cursor.rowcount > 0

        except Exception as e:
            conexion.rollback()
            print(f"Error al actualizar: {e}")
            return False

    def eliminar(self):
        conexion = ModelBase.__obtener_conexion()
        try:
            id_registro = self.model.get("id")
            if id_registro is None:
                print("No se puede eliminar un registro sin ID.")
                return False
            sql = f"DELETE FROM {self.__db_name}.{self.table_name} WHERE id = %s"
            cursor = conexion.cursor()
            cursor.execute(sql, (id_registro,))
            conexion.commit()

            return cursor.rowcount > 0

        except Exception as e:
            conexion.rollback()
            print(f"Error al eliminar: {e}")
            return False

    def obtener_por_id(self, id: int):
        conexion = ModelBase.__obtener_conexion()
        try:
            sql = f"SELECT * FROM {self.__db_name}.{self.table_name} WHERE id = %s"
            cursor = conexion.cursor()
            cursor.execute(sql, (id,))
            record = cursor.fetchone()
            if record:
                columnas = [desc[0] for desc in cursor.description]
                self.__model = dict(zip(columnas, record))
                return self.__model
            else:
                print(f"No se encontró ningún registro con ID {id} en {self.table_name}.")
                return None
        except Exception as e:
            print(f"Error al obtener: {e}")
            return None

