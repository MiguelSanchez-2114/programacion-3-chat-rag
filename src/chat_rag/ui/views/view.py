from abc import ABC, abstractmethod
from PySide6.QtWidgets import (
    QBoxLayout,
    QMainWindow,
    QWidget,
)

class ViewAbstract(ABC):

    @abstractmethod
    def build_ui(self):
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