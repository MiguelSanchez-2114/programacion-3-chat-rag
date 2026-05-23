from abc import ABC, abstractmethod
from PySide6.QtWidgets import (
    QBoxLayout,
    QMainWindow,
    QMessageBox,
    QWidget,
)

class ViewAbstract(ABC):

    @abstractmethod
    def build_ui(self):
        pass

    @abstractmethod
    def on_show(self):
        pass
    
class View(ViewAbstract):
    __main_window: QMainWindow
    __key: str
    __title: str
    __root: QBoxLayout
    __widgets: dict[str, QWidget]

    def __init__(self, window: QMainWindow, key: str, title: str):
        self.__main_window = window
        self.__key = key
        self.__title = title
        self.__widgets = {}

    @property
    def main_window(self) -> QMainWindow:
        return self.__main_window

    @property
    def key(self) -> str:
        return self.__key

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def root(self) -> QBoxLayout:
        return self.__root
    
    @root.setter
    def root(self, layout: QBoxLayout) -> None:
        self.__root = layout
    
    @property
    def widgets(self) -> dict[str, QWidget]:
        return self.__widgets

    def agregar_widget(self, clave: str, widget: QWidget) -> None:
        self.__widgets[clave] = widget

    def mostrar_mensaje(self, mensaje: str, titulo: str = "Chat RAG") -> None:
        QMessageBox.information(self.main_window, titulo, mensaje)

    def mostrar_error(self, mensaje: str, titulo: str = "Chat RAG") -> None:
        QMessageBox.critical(self.main_window, titulo, mensaje)
    
    def mostrar_confirmacion(self, mensaje: str, titulo: str = "Chat RAG", text_yes: str = "Sí", text_no: str = "No") -> bool:
        msg = QMessageBox(self.main_window)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)

        # Add buttons with custom text and roles
        accept_btn = msg.addButton(text_yes, QMessageBox.ButtonRole.AcceptRole)
        reject_btn = msg.addButton(text_no, QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        return msg.clickedButton() == accept_btn
