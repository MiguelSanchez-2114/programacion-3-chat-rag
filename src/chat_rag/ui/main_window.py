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
            QFrame#sidebar {
                background-color: #123A5F;
                border: none;
            }
            QLabel#appTitle {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: 750;
            }
            QLabel#sideText {
                color: #BFD4EC;
                font-size: 12px;
            }
            QLabel#sideSection {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
            }
            QLabel#fileName {
                color: #EAF3FF;
                background-color: #1E4E7D;
                border: 1px solid #326796;
                border-radius: 8px;
                padding: 9px;
            }
            QPushButton#sideButton {
                background-color: #FFFFFF;
                border: none;
                border-radius: 9px;
                color: #123A5F;
                font-size: 13px;
                font-weight: 700;
                padding: 10px;
                text-align: left;
            }
            QPushButton#sideButton:hover {
                background-color: #DCEBFF;
            }
            QFrame#chatPanel {
                background-color: #FFFFFF;
                border: 1px solid #D8E2EF;
                border-radius: 14px;
            }
            QLabel#chatTitle {
                color: #172033;
                font-size: 22px;
                font-weight: 750;
            }
            QLabel#chatSubtitle {
                color: #69778A;
                font-size: 12px;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget#conversationBody {
                background-color: #F8FBFF;
                border-radius: 12px;
            }
            QLabel#userBubble {
                background-color: #2563EB;
                border-radius: 13px;
                color: #FFFFFF;
                font-size: 14px;
                padding: 10px 14px;
            }
            QLabel#systemBubble {
                background-color: #FFFFFF;
                border: 1px solid #D8E2EF;
                border-radius: 13px;
                color: #263447;
                font-size: 14px;
                padding: 10px 14px;
            }
            QTextEdit#messageInput {
                background-color: #F8FBFF;
                border: 1px solid #CAD8EA;
                border-radius: 10px;
                color: #172033;
                font-size: 14px;
                padding: 8px;
            }
            QTextEdit#messageInput:focus {
                border: 2px solid #2F80ED;
                background-color: #FFFFFF;
            }
            QPushButton#sendButton {
                background-color: #7C3AED;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 750;
                padding: 12px 18px;
            }
            QPushButton#sendButton:hover {
                background-color: #6D28D9;
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

        # self.__main_layout.addWidget(self._create_sidebar())
        # self.__main_layout.addWidget(self._create_chat_panel(), stretch=1)

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
