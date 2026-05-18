from typing import Optional

from chat_rag.db.models.archivo_model import ArchivoModel


class Archivo:

    def __init__(self, id: Optional[int], nombre: str, tipo: str, tamano: str, id_conversacion: Optional[int]):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.tamano = tamano
        self.id_conversacion = id_conversacion

    @classmethod
    def desde_modelo(cls, modelo: "ArchivoModel") -> "Archivo":
        return cls(
            id=modelo.id,
            nombre=modelo.nombre,
            tipo=modelo.tipo,
            tamano=modelo.tamano,
            id_conversacion=modelo.id_conversacion
        )
    
    def guardar(self, id_conversacion: int):
        archivo_model = ArchivoModel({
            "nombre": self.nombre,
            "tipo": self.tipo,
            "tamano": self.tamano,
            "id_conversacion": id_conversacion
        })
        self.id = archivo_model.guardar()
        self.id_conversacion = id_conversacion

    def actualizar(self, id_conversacion: int):
        archivo_model = self.__obtener_por_id_conversacion(id_conversacion)
        if archivo_model is None:
            self.guardar(id_conversacion)
            return
        else:
            self.id = archivo_model.id
            archivo_model.nombre = self.nombre
            archivo_model.tipo = self.tipo
            archivo_model.tamano = self.tamano
            archivo_model.actualizar()
            self.id_conversacion = id_conversacion

    
    def __obtener_por_id_conversacion(self, id_conversacion: int) -> Optional["ArchivoModel"]:
        archivo_model = ArchivoModel.obtener_por_id_conversacion(id_conversacion)
        if archivo_model:
            return archivo_model
        return None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "tamano": self.tamano,
            "id_conversacion": self.id_conversacion
        }