import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from chat_rag.controllers.conversacion import Conversacion




class Exportador:

    @staticmethod
    def to_json(conversacion: Conversacion, indent: int = 2) -> str:
        
        data = conversacion.to_dict()
         
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def exportar_json(conversacion: Conversacion, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(Exportador.to_json(conversacion))

    @staticmethod
    def to_xml(conversacion: Conversacion) -> str:
        root = ET.Element("conversacion")
        root.set("id", str(conversacion.id))

        if conversacion.archivo:
            archivo_el = ET.SubElement(root, "archivo")
            archivo_el.text = conversacion.archivo.nombre
        
        mensajes_el = ET.SubElement(root, "mensajes")

        for mensaje in conversacion.mensajes:
            msg_el = ET.SubElement(mensajes_el, "mensaje")
            msg_el.set("emisor", mensaje.emisor)

            contenido_el = ET.SubElement(msg_el, "contenido")
            contenido_el.text = mensaje.contenido

            fecha_el = ET.SubElement(msg_el, "fecha")
            fecha_el.text = str(mensaje.fecha)

        raw = ET.tostring(root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="  ")

    @staticmethod
    def exportar_xml(conversacion: Conversacion, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(Exportador.to_xml(conversacion))


