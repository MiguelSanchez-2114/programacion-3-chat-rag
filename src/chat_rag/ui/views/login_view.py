from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
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
CLOUD_IMAGE = "nube_pixel transparente.png"  # asset nuevo, transparente
CLOUD_IMAGE_FALLBACK = "nube_pixel_transparente.png"
GRASS_IMAGE = "crayon_verde_transparente.png"


def asset_path(file_name: str) -> str:
    """Resuelve assets y permite fallback para nombres antiguos."""
    path = ASSETS_DIR / file_name
    if path.exists():
        return str(path)

    if file_name == CLOUD_IMAGE:
        fallback = ASSETS_DIR / CLOUD_IMAGE_FALLBACK
        if fallback.exists():
            return str(fallback)

    return str(path)


class PainterShell(QFrame):
    """Marco exterior con QPainter. Sin enmarcado rosa interno."""

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = QRectF(2, 2, self.width() - 4, self.height() - 4)
        path = QPainterPath()
        path.addRoundedRect(rect, 28, 28)

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.00, QColor("#78E7E4"))
        gradient.setColorAt(0.35, QColor("#F7A8E8"))
        gradient.setColorAt(0.70, QColor("#FFE873"))
        gradient.setColorAt(1.00, QColor("#63D99C"))
        painter.fillPath(path, gradient)

        # Borde exterior suave, no rosa dominante.
        painter.setPen(QPen(QColor("#7EE7E4"), 3))
        painter.drawPath(path)


class PainterLoginBackground(QFrame):
    """Lienzo principal: background rosa, bordes arcade y puntos decorativos."""

    DOTS = [
        (85, 165, "#FF9FC4"), (150, 215, "#7DDCE7"), (205, 180, "#61D779"),
        (270, 230, "#FFB0C8"), (365, 188, "#F38A00"), (450, 275, "#F7A4C4"),
        (570, 300, "#F5DE7A"), (690, 300, "#C681EE"), (810, 205, "#FF9FC4"),
        (880, 215, "#7DDCE7"), (960, 188, "#F38A00"), (1050, 230, "#61D779"),
        (1120, 290, "#7EDAEF"), (1245, 305, "#F7A4C4"), (1360, 245, "#F6DC7D"),
    ]

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        full_rect = QRectF(0, 0, self.width(), self.height())
        background_path = QPainterPath()
        background_path.addRoundedRect(full_rect.adjusted(1, 1, -1, -1), 20, 20)

        # Background rosa como base, con degradado muy leve para que no se vea plano.
        base_gradient = QLinearGradient(full_rect.topLeft(), full_rect.bottomRight())
        base_gradient.setColorAt(0.00, QColor("#FFF3FC"))
        base_gradient.setColorAt(0.48, QColor("#F9EAF7"))
        base_gradient.setColorAt(1.00, QColor("#F7E4F5"))
        painter.fillPath(background_path, base_gradient)

        self.__draw_inner_borders(painter, full_rect)
        self.__draw_waka_lines(painter)
        self.__draw_arcade_dots(painter)

    def __draw_inner_borders(self, painter: QPainter, full_rect: QRectF) -> None:
        # Se quitó el marco rosa interno. Quedan solo líneas cyan/amarillas.
        borders = [
            (QColor("#80E7E4"), 8, 5, 19),
            (QColor("#FFE873"), 16, 7, 15),
        ]

        painter.setBrush(Qt.NoBrush)
        for color, inset, width, radius in borders:
            painter.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRoundedRect(full_rect.adjusted(inset, inset, -inset, -inset), radius, radius)

    def __draw_waka_lines(self, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(QPen(QColor("#91EFD7"), 2))
        for x in range(240, 330, 8):
            painter.drawLine(x, 56, x + 4, 51)
            painter.drawLine(x + 4, 51, x + 8, 56)
        for x in range(1125, 1220, 8):
            painter.drawLine(x, 56, x + 4, 51)
            painter.drawLine(x + 4, 51, x + 8, 56)
        painter.setRenderHint(QPainter.Antialiasing, True)

    def __draw_arcade_dots(self, painter: QPainter) -> None:
        painter.setPen(Qt.NoPen)
        for x, y, color in self.DOTS:
            painter.setBrush(QColor(color))
            painter.drawEllipse(QRectF(x, y, 18, 18))


class GradientTextLabel(QLabel):
    """Texto de título/subtítulo con degradado pintado con QPainter."""

    def __init__(self, text: str, parent=None, font_size: int = 72, weight: int = QFont.Black):
        super().__init__(text, parent)
        self.font_size = font_size
        self.font_weight = weight
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        font = QFont("Segoe UI", self.font_size)
        font.setWeight(self.font_weight)
        painter.setFont(font)

        rect = QRectF(0, 0, self.width(), self.height())
        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.00, QColor("#8E7CF6"))
        gradient.setColorAt(0.45, QColor("#E98DDB"))
        gradient.setColorAt(1.00, QColor("#8FDDEA"))

        painter.setPen(QPen(gradient, 1))
        painter.drawText(rect, Qt.AlignCenter, self.text())


class DinoGradientButton(QPushButton):
    """Botón con gradiente, hover/pressed y texto dibujados con QPainter."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setMouseTracking(True)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        radius = rect.height() / 2

        start = QColor("#78D9ED")
        middle = QColor("#B56AF0")
        end = QColor("#7DE3D8")

        if self.isDown():
            start, middle, end = QColor("#58BCD8"), QColor("#9854D8"), QColor("#5CCDC3")
        elif self.underMouse():
            start, middle, end = QColor("#8BE9F5"), QColor("#CB7BFF"), QColor("#90EFE4")

        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.00, start)
        gradient.setColorAt(0.50, middle)
        gradient.setColorAt(1.00, end)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.fillPath(path, gradient)

        painter.setPen(QPen(QColor(255, 255, 255, 175), 1.4))
        painter.drawPath(path)

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Black)
        painter.setFont(font)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(rect, Qt.AlignCenter, self.text())


class DinoInput(QLineEdit):
    """Input con fondo/borde hecho con QPainter; mantiene edición normal."""

    def __init__(self, parent=None, border_color: str = "#58B66A", text_color: str = "#D7A216"):
        super().__init__(parent)
        self.border_color = QColor(border_color)
        self.text_color = QColor(text_color)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(
            f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {text_color};
                font-size: 15px;
                font-weight: 900;
                padding-left: 30px;
                padding-right: 18px;
                selection-background-color: #C982E9;
            }}
            """
        )

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = QRectF(3, 3, self.width() - 6, self.height() - 6)
        painter.setBrush(QColor(255, 255, 255, 230))

        pen = QPen(self.border_color, 4, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        if self.hasFocus():
            pen.setWidth(5)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 13, 13)

        super().paintEvent(event)


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

        shell = PainterShell()
        shell.setObjectName("loginShell")
        shell.setFixedSize(CANVAS_WIDTH + 16, CANVAS_HEIGHT + 16)

        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(8, 8, 8, 8)
        shell_layout.setSpacing(0)

        background = PainterLoginBackground()
        background.setObjectName("loginBackground")
        background.setFixedSize(CANVAS_WIDTH, CANVAS_HEIGHT)

        title = GradientTextLabel("DiNO Chat", background, font_size=78, weight=QFont.Black)
        title.setObjectName("dinoTitle")
        title.setAlignment(Qt.AlignCenter)

        slogan = GradientTextLabel('"Work smarter, not harder"', background, font_size=30, weight=QFont.ExtraBold)
        slogan.setObjectName("dinoSlogan")
        slogan.setAlignment(Qt.AlignCenter)

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
        self.__position_text()
        self.__position_login_controls()

    def __build_login_controls(self, background: QFrame) -> None:
        username_input = DinoInput(background, border_color="#5EB66D", text_color="#D9A51D")
        username_input.setObjectName("dinoInputOverlay")
        username_input.setPlaceholderText("Enter your username")
        username_input.focusInEvent = lambda event: self.__clear_error_message()

        password_input = DinoInput(background, border_color="#4D9BDF", text_color="#58B66D")
        password_input.setObjectName("dinoInputOverlay")
        password_input.setPlaceholderText("Enter your password")
        password_input.setEchoMode(QLineEdit.Password)

        login_button = DinoGradientButton("Login", background)
        login_button.setObjectName("dinoLoginButton")
        login_button.clicked.connect(self._validate_login)
        password_input.returnPressed.connect(self._validate_login)

        error_label = QLabel("", background)
        error_label.setObjectName("dinoError")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.hide()

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
        image.setPixmap(QPixmap(asset_path(file_name)))

        self.agregar_widget(key, image)
        return image

    def __build_decorations(self, background: QFrame) -> None:
        self.__build_image(background, "cloud_left", CLOUD_IMAGE, 190, 110)
        self.__build_image(background, "cloud_top_left", CLOUD_IMAGE, 220, 125)
        self.__build_image(background, "cloud_right", CLOUD_IMAGE, 205, 118)
        self.__build_image(background, "cloud_top_right", CLOUD_IMAGE, 190, 110)

        self.__build_image(background, "dino_image", DINO_IMAGE, 365, 365)
        self.__build_image(background, "grass_image", GRASS_IMAGE, 520, 64)

        self.__build_image(background, "username_icon", PACMAN_IMAGE, 62, 62)
        self.__build_image(background, "password_icon", RED_GHOST_IMAGE, 62, 62)

        for index in range(1, 6):
            self.__build_image(background, f"left_blue_ghost_{index}", BLUE_GHOST_IMAGE, 52, 52)
            self.__build_image(background, f"right_blue_ghost_{index}", BLUE_GHOST_IMAGE, 52, 52)

    def __position_assets(self) -> None:
        self.widgets["cloud_left"].move(70, 82)
        self.widgets["cloud_top_left"].move(255, 40)
        self.widgets["cloud_right"].move(990, 92)
        self.widgets["cloud_top_right"].move(1212, 46)

        self.widgets["dino_image"].move(540, 220)
        self.widgets["grass_image"].move(462, 505)

        # Inputs/icons quedan dentro del área útil; nada se sale del marco inferior.
        self.widgets["username_icon"].move(465, 580)
        self.widgets["password_icon"].move(465, 650)

        left_ghost_x = [55, 125, 195, 265, 335]
        right_ghost_x = [1035, 1105, 1175, 1245, 1315]

        for index, x in enumerate(left_ghost_x, start=1):
            self.widgets[f"left_blue_ghost_{index}"].move(x, 655)

        for index, x in enumerate(right_ghost_x, start=1):
            self.widgets[f"right_blue_ghost_{index}"].move(x, 655)

        for key in (
            "cloud_left",
            "cloud_top_left",
            "cloud_right",
            "cloud_top_right",
            "dino_image",
            "grass_image",
            "username_icon",
            "password_icon",
            "left_blue_ghost_1",
            "left_blue_ghost_2",
            "left_blue_ghost_3",
            "left_blue_ghost_4",
            "left_blue_ghost_5",
            "right_blue_ghost_1",
            "right_blue_ghost_2",
            "right_blue_ghost_3",
            "right_blue_ghost_4",
            "right_blue_ghost_5",
        ):
            self.widgets[key].raise_()

    def __position_text(self) -> None:
        title = self.widgets["title_label"]
        title.setFixedSize(900, 100)
        title.move(274, 36)

        slogan = self.widgets["slogan_label"]
        slogan.setFixedSize(940, 56)
        slogan.move(254, 122)

        for key in ("title_label", "slogan_label"):
            self.widgets[key].raise_()

    def __position_login_controls(self) -> None:
        username_input = self.widgets["username_input"]
        username_input.setFixedSize(360, 54)
        username_input.move(540, 580)

        password_input = self.widgets["password_input"]
        password_input.setFixedSize(360, 54)
        password_input.move(540, 650)

        login_button = self.widgets["login_button"]
        login_button.setFixedSize(210, 46)
        login_button.move(1120, 604)

        error_label = self.widgets["error_label"]
        error_label.setFixedSize(360, 24)
        error_label.move(540, 626)

        for key in ("username_input", "password_input", "login_button", "error_label"):
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
            error_label.hide()
            self.main_window.route("chat")
            return

        error_label.setText("Usuario o contraseña incorrectos")
        error_label.show()
        password_input.clear()
        password_input.setFocus()

    def __apply_login_styles(self) -> None:
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #FBE8F8;
                font-family: Segoe UI, Arial, sans-serif;
            }

            QScrollArea#loginScrollArea,
            QScrollArea#loginScrollArea > QWidget,
            QScrollArea#loginScrollArea > QWidget > QWidget {
                background-color: #FBE8F8;
                border: none;
            }

            QPushButton#dinoLoginButton {
                border: none;
                color: #FFFFFF;
                background: transparent;
            }

            QLabel#dinoError {
                color: #D7365E;
                font-size: 12px;
                font-weight: 800;
                background-color: transparent;
                border: none;
            }
            """
        )

    def __clear_error_message(self) -> None:
        error_label = self.widgets["error_label"]
        error_label.setText("")