import sys

from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget
)

from PySide6.QtCore import Qt

from chat_rag.ui.views.view import View

class MainWindow(QMainWindow):
    __title: str
    __views: dict[str, View]
    __main_layout: QBoxLayout

    def __init__(self) -> None:
        super().__init__()
        self.__title = "Chat RAG"
        self.__views = {}
        self.__main_layout = None
        self.setWindowTitle(self.__title)
        self.resize(980, 680)

        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        self.__main_layout = QVBoxLayout()
        root.setLayout(self.__main_layout)

        # Texto de referencia.
        workarea_label = QLabel("Área de trabajo")
        workarea_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        workarea_label.setAlignment(Qt.AlignCenter)
        self.__main_layout.addWidget(workarea_label)

        # self.__load_views()
    
    def __load_views(self) -> None:
        views = []
        self.__views = {view.key: view for view in views}
        self.__current_view = views[0]
        self.__update_view()
    
    def __update_view(self) -> None:
        if self.__current_view is not None:
            # Limpiar el layout actual.
            while self.__main_layout.count():
                child = self.__main_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            # Agregar la vista actual al layout.
            self.__main_layout.addLayout(self.__current_view.root)
            self.__update_title(self.__current_view.title)

    def __update_title(self, subtitle: str) -> None:
        title = f"{self.__title}"
        if subtitle:
            title += f" - {subtitle}"
        self.setWindowTitle(title)

    def __switch_view(self, key: str) -> None:
        if self.__exist_view(key):
            self.__current_view = self.__views[key]
            self.__update_view()

    def __exist_view(self, key: str) -> bool:
        return key in self.__views
    
    def route(self, key: str) -> None:
        if self.__exist_view(key):
            self.__switch_view(key)

def run_app() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
