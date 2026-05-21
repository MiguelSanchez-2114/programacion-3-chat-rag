import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from chat_rag.domain.conversacion import Conversacion


class Exportador:

    @staticmethod
    def to_json(conversacion: Conversacion, indent: int = 2) -> str:
        data = {
            "id": conversacion.id,
            "id_usuario": conversacion.id_usuario,
            "mensajes": [
                {
                    "contenido": mensaje.contenido,
                    "emisor": mensaje.emisor,
                    "id_conversacion": mensaje.id_conversacion,
                }
                for mensaje in conversacion.mensajes
            ],
        }
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def exportar_json(conversacion: Conversacion, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(Exportador.to_json(conversacion))

    @staticmethod
    def to_xml(conversacion: Conversacion) -> str:
        root = ET.Element("conversacion")
        root.set("id", str(conversacion.id))
        root.set("id_usuario", str(conversacion.id_usuario))

        mensajes_el = ET.SubElement(root, "mensajes")
        for mensaje in conversacion.mensajes:
            msg_el = ET.SubElement(mensajes_el, "mensaje")
            msg_el.set("emisor", mensaje.emisor)
            ET.SubElement(msg_el, "contenido").text = mensaje.contenido
            ET.SubElement(msg_el, "id_conversacion").text = str(mensaje.id_conversacion)

        raw = ET.tostring(root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="  ")

    @staticmethod
    def exportar_xml(conversacion: Conversacion, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(Exportador.to_xml(conversacion))


