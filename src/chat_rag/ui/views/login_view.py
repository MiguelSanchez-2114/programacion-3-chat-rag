import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from chat_rag.ui.views.view import View

class LoginView(View):
    def __init__(self, window: QMainWindow):
        super().__init__(window, key="login", title="Login")
        self.main_window.resize(500, 620)
        self.main_window.setMinimumSize(460, 590)
        self.build_ui()

    def build_ui(self) -> None:
        self.root = QVBoxLayout()
        self.root.setContentsMargins(34, 28, 34, 28)
        self.root.setSpacing(18)

        self.main_window.setStyleSheet(
            """
            QDialog {
                background-color: #EEF4FF;
                color: #1D2738;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QLabel#brandTitle {
                color: #143A63;
                font-size: 30px;
                font-weight: 700;
            }
            QLabel#brandSubtitle {
                color: #64748B;
                font-size: 13px;
            }
            QFrame#loginCard {
                background-color: #FFFFFF;
                border: 1px solid #D7E3F5;
                border-radius: 18px;
            }
            QLabel#sectionTitle {
                color: #1D2738;
                font-size: 22px;
                font-weight: 650;
            }
            QLabel#fieldLabel {
                color: #334155;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #F8FBFF;
                border: 1px solid #CAD8EA;
                border-radius: 10px;
                color: #1D2738;
                font-size: 14px;
                padding: 10px 12px;
            }
            QLineEdit:focus {
                border: 2px solid #2F80ED;
                background-color: #FFFFFF;
            }
            QPushButton#loginButton {
                background-color: #2563EB;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 15px;
                font-weight: 700;
                padding: 12px;
            }
            QPushButton#loginButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton#loginButton:pressed {
                background-color: #1E40AF;
            }
            QLabel#errorLabel {
                color: #D64545;
                font-size: 12px;
                font-weight: 600;
                min-height: 18px;
            }
            QLabel#hintLabel {
                color: #7C8AA3;
                font-size: 12px;
            }
            QWidget#accentBar {
                background-color: #7C3AED;
                border-radius: 6px;
            }
            """
        )

        header = QVBoxLayout()
        header.setSpacing(4)

        brand_title = QLabel("Chat RAG")
        brand_title.setObjectName("brandTitle")
        brand_title.setAlignment(Qt.AlignCenter)

        brand_subtitle = QLabel("Consulta documentos desde una experiencia tipo chat")
        brand_subtitle.setObjectName("brandSubtitle")
        brand_subtitle.setAlignment(Qt.AlignCenter)

        header.addWidget(brand_title)
        header.addWidget(brand_subtitle)
        self.root.addLayout(header)

        card = QFrame()
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 24)
        card_layout.setSpacing(14)

        accent_row = QHBoxLayout()
        accent_row.setAlignment(Qt.AlignCenter)
        accent_bar = QWidget()
        accent_bar.setObjectName("accentBar")
        accent_bar.setFixedSize(76, 6)
        accent_row.addWidget(accent_bar)

        section_title = QLabel("Inicio de sesion")
        section_title.setObjectName("sectionTitle")
        section_title.setAlignment(Qt.AlignCenter)

        section_hint = QLabel("Ingresa tus credenciales para continuar")
        section_hint.setObjectName("hintLabel")
        section_hint.setAlignment(Qt.AlignCenter)

        card_layout.addLayout(accent_row)
        card_layout.addWidget(section_title)
        card_layout.addWidget(section_hint)
        card_layout.addSpacing(8)

        user_label = QLabel("Usuario")
        user_label.setObjectName("fieldLabel")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ej. admin")
        self.username_input.setMinimumHeight(42)

        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Escribe tu password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(42)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Ingresar")
        self.login_button.setObjectName("loginButton")
        self.login_button.setMinimumHeight(46)
        self.login_button.clicked.connect(self._validate_login)
        self.password_input.returnPressed.connect(self._validate_login)

        card_layout.addWidget(user_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(self.login_button)

        self.root.addWidget(card)

        footer = QLabel("Proyecto academico - Programacion")
        footer.setObjectName("hintLabel")
        footer.setAlignment(Qt.AlignCenter)
        self.root.addWidget(footer)

    def _validate_login(self) -> None:
        expected_user = os.getenv("APP_USERNAME", "admin")
        expected_password = os.getenv("APP_PASSWORD", "admin123")

        username = self.username_input.text().strip()
        password = self.password_input.text()

        if username == expected_user and password == expected_password:
            self.accept()
            return

        self.error_label.setText("Usuario o password incorrectos")
        self.password_input.clear()
        self.password_input.setFocus()
