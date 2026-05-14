import os
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)

from chat_rag.ui.views.view import View
from chat_rag.controllers.autorizacion import Autorizacion

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"

CANVAS_WIDTH = 1447
CANVAS_HEIGHT = 736

DINO_IMAGE = "dino_transparente.png"
PACMAN_IMAGE = "pacman_fondo_negro_transparente.png"
RED_GHOST_IMAGE = "fantasma_rojo_pixel_transparente.png"
BLUE_GHOST_IMAGE = "fantasma_azul_transparente.png"
CLOUD_IMAGE = "nube_pixel_transparente.png"
GRASS_IMAGE = "crayon_verde_transparente.png"


class LoginView(View):
    def __init__(self, window: QMainWindow):
        super().__init__(window, key="login", title="Login")
        self.main_window.resize(CANVAS_WIDTH + 180, CANVAS_HEIGHT + 160)
        self.main_window.setMinimumSize(1100, 720)
        self.auth = Autorizacion()
        self.build_ui()

    def build_ui(self) -> None:
        self.root = QVBoxLayout()
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(0)
        
        self.__apply_login_styles()

        shell = QFrame()
        shell.setObjectName("loginShell")
        shell.setFixedSize(CANVAS_WIDTH + 16, CANVAS_HEIGHT + 16)

        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(8, 8, 8, 8)
        shell_layout.setSpacing(0)

        background = QFrame()
        background.setObjectName("loginBackground")
        background.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)
        background.setStyleSheet(
            """
            QFrame#loginBackground {
            border: none;
            border-radius: 18px;
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 1, y2: 1,
                stop: 0 #FFF7FC,
                stop: 0.50 #F8EEF8,
                stop: 1 #E8F0E6
        );

            }
            """
        )


        title = QLabel("DiNO Chat", background)
        title.setObjectName("dinoTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2F2F2F; font-size: 84px; font-weight: 900;")

        slogan = QLabel('"Work smarter, not harder"', background)
        slogan.setObjectName("dinoSlogan")
        slogan.setAlignment(Qt.AlignCenter)
        slogan.setStyleSheet("color: #2F2F2F; font-size: 38px; font-weight: 850;")

        shell_layout.addWidget(background)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("loginScrollArea")
        scroll_area.setWidgetResizable(False)
        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_area.setWidget(shell)
        self.root.addWidget(scroll_area)

        self.agregar_widget("login_shell", shell)
        self.agregar_widget("login_scroll_area", scroll_area)
        
        self.agregar_widget("login_background", background)
        self.agregar_widget("title_label", title)
        self.agregar_widget("slogan_label", slogan)
        

        self.__build_decorations(background)
        self.__build_login_controls(background)
        self.__position_assets()
        self.__position_text(background)
        self.__position_login_controls(background)

    def __build_login_controls(self, background: QFrame) -> None:
        username_input = QLineEdit(background)
        username_input.setObjectName("dinoInputOverlay")
        username_input.setPlaceholderText("Enter your username")
        username_input.focusInEvent = lambda event: self.__clear_error_message()

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
        error_label.setAlignment(Qt.AlignLeft)

        self.agregar_widget("username_input", username_input)
        self.agregar_widget("password_input", password_input)
        self.agregar_widget("login_button", login_button)
        self.agregar_widget("error_label", error_label)
    
    def __build_image(
        self,
        background: QFrame,
        key: str,
        file_name: str,
        width: int,
        height: int,
    ) -> QLabel:
        image = QLabel(background)
        image.setObjectName(key)
        image.setFixedSize(width, height)
        image.setScaledContents(True)
        image.setPixmap(QPixmap(str(ASSETS_DIR / file_name)))

        self.agregar_widget(key, image)
        return image
    
    def __build_decorations(self, background: QFrame) -> None:
        self.__build_image(background, "cloud_left", CLOUD_IMAGE, 210, 120)
        self.__build_image(background, "cloud_top_left", CLOUD_IMAGE, 235, 135)
        self.__build_image(background, "cloud_right", CLOUD_IMAGE, 220, 125)
        self.__build_image(background, "cloud_top_right", CLOUD_IMAGE, 200, 115)

        self.__build_image(background, "dino_image", DINO_IMAGE, 400, 400)
        self.__build_image(background, "grass_image", GRASS_IMAGE, 560, 70)

        self.__build_image(background, "username_icon", PACMAN_IMAGE, 70, 70)
        self.__build_image(background, "password_icon", RED_GHOST_IMAGE, 70, 70)

        for index in range(1, 6):
            self.__build_image(background, f"left_blue_ghost_{index}", BLUE_GHOST_IMAGE, 58, 58)
            self.__build_image(background, f"right_blue_ghost_{index}", BLUE_GHOST_IMAGE, 58, 58)

    def __position_assets(self) -> None:
        self.widgets["cloud_left"].move(60, 70)
        self.widgets["cloud_top_left"].move(250, 25)
        self.widgets["cloud_right"].move(990, 80)
        self.widgets["cloud_top_right"].move(1200, 35)

        self.widgets["dino_image"].move(524, 170)
        self.widgets["grass_image"].move(406, 507)

        self.widgets["username_icon"].move(485, 590)
        self.widgets["password_icon"].move(485, 670)


        left_ghost_x = [35, 105, 175, 245, 315]
        right_ghost_x = [1030, 1100, 1170, 1240, 1310]


        for index, x in enumerate(left_ghost_x, start=1):
            self.widgets[f"left_blue_ghost_{index}"].move(x, 665)

        for index, x in enumerate(right_ghost_x, start=1):
            self.widgets[f"right_blue_ghost_{index}"].move(x, 665)

        for key in (
            "cloud_left",
            "cloud_top_left",
            "cloud_right",
            "cloud_top_right",
            "dino_image",
            "username_icon",
            "password_icon",
            "left_blue_ghost_1",
            "left_blue_ghost_2",
            "left_blue_ghost_3",
            "right_blue_ghost_1",
            "right_blue_ghost_2",
            "right_blue_ghost_3",
            "right_blue_ghost_4",
            "right_blue_ghost_5",
            "left_blue_ghost_4",
            "left_blue_ghost_5",

        ):
            self.widgets[key].raise_()

    def __position_text(self, background: QFrame) -> None:
        title = self.widgets["title_label"]
        title.setFixedSize(900, 105)
        title.move(274, 38)

        slogan = self.widgets["slogan_label"]
        slogan.setFixedSize(940, 58)
        slogan.move(254, 128)
        for key in ("title_label", "slogan_label"):
            self.widgets[key].raise_()   

    def __position_login_controls(self, background: QFrame) -> None:
        username_input = self.widgets["username_input"]
        username_input.setFixedSize(200, 42)
        username_input.move(558, 605)

        password_input = self.widgets["password_input"]
        password_input.setFixedSize(200, 42)
        password_input.move(558, 687)

        login_button = self.widgets["login_button"]
        login_button.setFixedSize(188, 44)
        login_button.move(1115, 590)

        error_label = self.widgets["error_label"]
        error_label.setFixedSize(430, 24)
        error_label.move(780, 620)

        for key in (
            "username_input",
            "password_input",
            "login_button",
            "error_label",
        ):
            self.widgets[key].raise_()
        
    def _validate_login(self) -> None:
        username_input = self.widgets["username_input"]
        password_input = self.widgets["password_input"]
        error_label = self.widgets["error_label"]

        username = username_input.text().strip()
        password = password_input.text()

        usuario = self.auth.login(username=username, password=password)

        if usuario:
            error_label.setText("")
            self.main_window.route("chat")
            return

        error_label.setText("Usuario o contraseña incorrectos")
        password_input.clear()
        password_input.setFocus()

    def __apply_login_styles(self) -> None:
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #F7A8E8;
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
                font-size: 72px;
                font-weight: 900;
                letter-spacing: 0px;
            }

            QLabel#dinoSlogan {
                color: #2F2F2F;
                font-size: 34px;
                font-weight: 850;
                letter-spacing: 0px;
            }

            QLabel#dinoFooter {
                color: #2F2F2F;
                font-size: 15px;
                font-weight: 850;
            }python
           
            QLineEdit#dinoInputOverlay {
                background-color: #F1C3FF;
                border: 2px solid #D58BEF;
                border-radius: 16px;
                color: #2F2234;
                font-size: 14px;
                font-weight: 700;
                padding-left: 22px;
                padding-right: 18px;
            }


            QLineEdit#dinoInputOverlay::placeholder {
                color: #3A2A45;
            }

            QLineEdit#dinoInputOverlay {
                background-color: #FFE873;
                border: 2px solid #D8A900;
                border-radius: 16px;
                color: #2B2200;
                font-size: 14px;
                font-weight: 700;
                padding-left: 22px;
                padding-right: 18px;
            }

            QPushButton#dinoLoginButton {
                background-color: #8ACFE8;
                border: none;
                border-radius: 17px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 850;
            }

            QScrollArea#loginScrollArea {
                background-color: #BFEFFF;
                border: none;
            }

            QScrollArea#loginScrollArea > QWidget {
                background-color: #BFEFFF;
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

    def __clear_error_message(self) -> None:
        error_label = self.widgets["error_label"]
        error_label.setText("")