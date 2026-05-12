import os
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from chat_rag.ui.views.view import View

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
LOGIN_BACKGROUND = ASSETS_DIR / "fondo_login.png"


class LoginView(View):
    def __init__(self, window: QMainWindow):
        super().__init__(window, key="login", title="Login")
        self.main_window.resize(980, 680)
        self.main_window.setMinimumSize(900, 540)
        self.build_ui()

    def build_ui(self) -> None:
        self.root = QVBoxLayout()
        self.root.setContentsMargins(22, 22, 22, 22)
        self.root.setSpacing(0)

        self.__apply_login_styles()


        shell = QFrame()
        shell.setObjectName("loginShell")
        shell.setMinimumSize(900, 540)
        shell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(8, 8, 8, 8)
        shell_layout.setSpacing(0)

        background = QFrame()
        background.setObjectName("loginBackground")
        background.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        background.setStyleSheet(
            f"""
            QFrame#loginBackground {{
                border: none;
                border-radius: 18px;
                border-image: url("{LOGIN_BACKGROUND.as_posix()}") 0 0 0 0 stretch stretch;
            }}
            """
        )

        title = QLabel("DiNO Chat", background)
        title.setObjectName("dinoTitle")
        title.setAlignment(Qt.AlignCenter)

        slogan = QLabel('"Work smarter, not harder"', background)
        slogan.setObjectName("dinoSlogan")
        slogan.setAlignment(Qt.AlignCenter)


        shell_layout.addWidget(background)
        self.root.addWidget(shell)

        self.agregar_widget("login_shell", shell)
        self.agregar_widget("login_background", background)
        self.agregar_widget("title_label", title)
        self.agregar_widget("slogan_label", slogan)
        

        self.__build_login_controls(background)
        self.__position_text(background)
        self.__position_login_controls(background)

        previous_resize_event = background.resizeEvent

        def resize_event(event):
            previous_resize_event(event)
            self.__position_text(background)
            self.__position_login_controls(background)

        background.resizeEvent = resize_event
        
    def __build_login_controls(self, background: QFrame) -> None:
        username_input = QLineEdit(background)
        username_input.setObjectName("dinoInputOverlay")
        username_input.setPlaceholderText("Enter your username")

        password_input = QLineEdit(background)
        password_input.setObjectName("dinoInputOverlay")
        password_input.setPlaceholderText("Enter your password")
        password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login", background)
        login_button.setObjectName("dinoLoginButton")
        login_button.clicked.connect(self._validate_login)
        password_input.returnPressed.connect(self._validate_login)

        error_label = QLabel("", background)
        error_label.setObjectName("dinoError")
        error_label.setAlignment(Qt.AlignCenter)

        self.agregar_widget("username_input", username_input)
        self.agregar_widget("password_input", password_input)
        self.agregar_widget("login_button", login_button)
        self.agregar_widget("error_label", error_label)
        
    def __position_text(self, background: QFrame) -> None:
        width = background.width()
        height = background.height()

        title_width = int(width * 0.36)
        title_x = (width - title_width) // 2

        title = self.widgets["title_label"]
        title.setFixedSize(title_width, max(44, int(height * 0.075)))
        title.move(title_x, int(height * 0.045))

        slogan = self.widgets["slogan_label"]
        slogan.setFixedSize(title_width, max(28, int(height * 0.048)))
        slogan.move(title_x, int(height * 0.118))

        for key in ("title_label", "slogan_label"):
            self.widgets[key].raise_()


    def __position_login_controls(self, background: QFrame) -> None:
        width = background.width()
        height = background.height()

        input_x = int(width * 0.390)
        input_width = int(width * 0.285)
        input_height = max(38, int(height * 0.072))
        username_y = int(height * 0.705)
        password_y = int(height * 0.845)


        username_input = self.widgets["username_input"]
        username_input.setFixedSize(input_width, input_height)
        username_input.move(input_x, username_y)

        password_input = self.widgets["password_input"]
        password_input.setFixedSize(input_width, input_height)
        password_input.move(input_x, password_y)

        login_button = self.widgets["login_button"]
        login_button.setFixedSize(int(width * 0.13), max(32, int(height * 0.052)))
        login_button.move(int(width * 0.825), int(height * 0.806))

        error_label = self.widgets["error_label"]
        error_label.setFixedSize(input_width, 22)
        error_label.move(input_x, min(height - 32, password_y + input_height + 10))

        for key in (
            "username_input",
            "password_input",
            "login_button",
            "error_label",
        ):
            self.widgets[key].raise_()
            
    def _validate_login(self) -> None:
        expected_user = "admin"
        expected_password = "admin123"

        username_input = self.widgets["username_input"]
        password_input = self.widgets["password_input"]
        error_label = self.widgets["error_label"]

        username = username_input.text().strip()
        password = password_input.text()

        if username == expected_user and password == expected_password:
            error_label.setText("")
            self.main_window.route("chat")
            return

        error_label.setText("Invalid username or password")
        password_input.clear()
        password_input.setFocus()

    def __apply_login_styles(self) -> None:
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #F2F8FF;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QFrame#loginShell {
                border-radius: 24px;
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #73C6D8,
                    stop: 0.48 #F4D7EF,
                    stop: 1 #5B8C66
                );
            }
            QLabel#dinoTitle {
                color: #2F2F2F;
                font-size: 40px;
                font-weight: 900;
                letter-spacing: 0px;
            }
            QLabel#dinoSlogan {
                color: #2F2F2F;
                font-size: 23px;
                font-weight: 850;
                letter-spacing: 0px;
            }
            QLabel#dinoFooter {
                color: #2F2F2F;
                font-size: 15px;
                font-weight: 850;
            }
           QLineEdit#dinoInputOverlay {
              background-color: transparent;
              border: none;
              color: #151515;
              font-size: 16px;
              font-weight: 650;
              padding-left: 34px;
              padding-right: 24px;
            }
            
            QLineEdit#dinoInputOverlay::placeholder {
            color: #3A2A45;
            }

            QLineEdit#dinoInputOverlay:focus {
                border: none;
                background-color: rgba(255, 255, 255, 35);
            }
            
            QPushButton#dinoLoginButton {
                background-color: #8ACFE8;
                border: none;
                border-radius: 15px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 800;
            }
            QPushButton#dinoLoginButton:hover {
                background-color: #72C3E2;
            }
            QPushButton#dinoLoginButton:pressed {
                background-color: #5AB4D8;
            }
            QLabel#dinoError {
                color: #C83D3D;
                font-size: 12px;
                font-weight: 700;
            }
            """
        )
