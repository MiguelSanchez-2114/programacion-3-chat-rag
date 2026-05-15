import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

from PySide6.QtCore import Qt

from chat_rag.ui.views.login_view import LoginView
from chat_rag.ui.views.chat_view import ChatView
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
        self.loaded_file_name = None
    
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F4F7FB;
                color: #172033;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QWidget#root {
                background-color: #F4F7FB;
            }
            """
        )

        root = QWidget()        
        root.setObjectName("root")
        self.setCentralWidget(root)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(18, 18, 18, 18)
        self.__main_layout.setSpacing(16)
        root.setLayout(self.__main_layout)

        # Texto de referencia.
        workarea_label = QLabel("Área de trabajo")
        workarea_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        workarea_label.setAlignment(Qt.AlignCenter)
        self.__main_layout.addWidget(workarea_label)
        self.__load_views()

    def __load_views(self) -> None:
        views = [
            LoginView(window=self),
            ChatView(window=self),
        ]

        self.__views = {view.key: view for view in views}
        self.__current_view = views[0]
        self.__update_view()
    
    def __update_view(self) -> None:
        if self.__current_view is not None:
            # Limpiar el layout actual.
            self.__clear_layout(self.__main_layout)
            # Agregar la vista actual al layout.
            self.__main_layout.addLayout(self.__current_view.root)
            self.__update_title(self.__current_view.title)

    def __clear_layout(self, layout: QBoxLayout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            widget = child.widget()
            child_layout = child.layout()

            if widget is not None:
                widget.deleteLater()

            if child_layout is not None:
                self.__clear_layout(child_layout)

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
