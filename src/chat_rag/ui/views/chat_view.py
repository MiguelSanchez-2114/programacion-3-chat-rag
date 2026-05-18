from pathlib import Path
from typing import Optional

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.controllers.manejador_archivo import ManejadorArchivo
from chat_rag.controllers.archivo import Archivo
from chat_rag.controllers.chat import Chat
from chat_rag.controllers.modelo_ia import ModeloIA
from chat_rag.ui.views.view import View

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
CHAT_CANVAS_WIDTH = 1447
CHAT_CANVAS_HEIGHT = 736
CACTUS_PACMAN_IMAGE = "cactus_pacman_transparente.png"
GRASS_IMAGE = "crayon_verde_transparente.png"
YELLOW_GRASS_IMAGE = "pasto_amarillo_transparente.png"
DINO_IMAGE = "dino_transparente.png"
DINO_PURPLE_IMAGE = "dino_morado_transparente.png"
BLUE_GHOST_IMAGE = "fantasma_azul_transparente.png"
RED_GHOST_IMAGE = "fantasma_rojo_pixel_transparente.png"


class GradientTitleLabel(QLabel):
    """Large rounded title painted with a playful multi-color gradient."""

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        font = QFont("Arial Rounded MT Bold", 46)
        font.setWeight(QFont.Weight.Black)
        painter.setFont(font)

        metrics = QFontMetrics(font)
        text = self.text()
        text_rect = metrics.boundingRect(text)
        x = (self.width() - text_rect.width()) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2

        path = QPainterPath()
        path.addText(x, y, font, text)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.00, QColor("#7AF7E1"))
        gradient.setColorAt(0.22, QColor("#6B57FF"))
        gradient.setColorAt(0.48, QColor("#F38BDA"))
        gradient.setColorAt(0.72, QColor("#7E4DFF"))
        gradient.setColorAt(1.00, QColor("#5DEFE0"))

        painter.fillPath(path, gradient)


class ConfettiLayer(QFrame):
    """Decorative confetti painted directly on the chat canvas."""

    DOTS = (
        (155, 146, 22, "#FFB3D1"),
        (232, 124, 20, "#FF8A00"),
        (318, 148, 22, "#FFB3D1"),
        (386, 132, 22, "#FF8A00"),
        (910, 154, 22, "#FFB3D1"),
        (962, 172, 22, "#9DEBFF"),
        (1088, 184, 22, "#FF8A00"),
        (112, 314, 22, "#FFB3D1"),
        (220, 288, 22, "#9DEBFF"),
        (318, 296, 22, "#FFE899"),
        (502, 372, 22, "#FFE899"),
        (545, 318, 22, "#FF8A00"),
        (802, 226, 22, "#FFB3D1"),
        (925, 226, 22, "#FFE899"),
        (984, 220, 22, "#FFB3D1"),
        (210, 338, 22, "#FFB3D1"),
        (332, 396, 22, "#9DEBFF"),
        (448, 470, 22, "#FFB3D1"),
        (650, 500, 22, "#FF8A00"),
        (925, 475, 22, "#FFB3D1"),
        (1030, 500, 22, "#9DEBFF"),
        (1092, 528, 22, "#FFE899"),
        (1125, 528, 22, "#FF8A00"),
    )

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        for x, y, size, color in self.DOTS:
            painter.setBrush(QColor(color))
            painter.drawEllipse(QRectF(x, y, size, size))


class DecorativePanelFrame(QFrame):
    """Rounded purple frame around the fixed chat canvas."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#B846D2"), 5)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(4, 4, self.width() - 8, self.height() - 8), 28, 28)


class MessageBubble(QFrame):
    """Hand-drawn chat bubble painted with QPainter."""

    VISUAL_VARIANTS = {
        "bot": {
            "outline": "#8FEFD6",
            "hatch": "#8FEFD6",
            "text": "#5C4A57",
            "fill": "#B5F1BE",
            "tail_side": "left",
        },
        "usuario": {
            "outline": "#FFC0D8",
            "hatch": "#FFC0D8",
            "text": "#5C4A57",
            "fill": "#CDBBFF",
            "tail_side": "right",
        },
    }

    def __init__(self, message: str, sender: str = "bot", date: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__message = message
        self.__sender = sender
        self.__date = date or "Ahora"
        self.__max_text_width = 480
        self.__min_bubble_width = 560
        self.__max_bubble_width = 650
        self.__min_bubble_height = 90
        self.__outline_width = 5
        self.__hatch_gap = 6
        self.__min_font_size = 9
        self.__max_font_size = 13

        self.setObjectName("messageBubble")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(self.__min_bubble_width)
        self.setMaximumWidth(self.__max_bubble_width)
        self.__fit_bubble_to_text()

    # Functional methods.
    def set_message(self, message: str) -> None:
        self.__message = message
        self.__fit_bubble_to_text()
        self.update()

    def set_sender(self, sender: str) -> None:
        if sender not in self.VISUAL_VARIANTS:
            sender = "bot"

        self.__sender = sender
        self.update()

    def message(self) -> str:
        return self.__message

    def sender(self) -> str:
        return self.__sender

    def date(self) -> str:
        return self.__date

    def sizeHint(self) -> QSize:
        return QSize(self.width(), self.height())

    # Visual methods.
    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = self.__build_bubble_path()
        self.__draw_bubble_background(painter, path)
        self.__draw_hatch_pattern(painter, path)
        self.__draw_bubble_outline(painter, path)
        self.__draw_message_text(painter)

    def __visual_config(self) -> dict[str, str]:
        return self.VISUAL_VARIANTS.get(self.__sender, self.VISUAL_VARIANTS["bot"])

    def __build_bubble_path(self) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(self.__bubble_body_rect(""), 18, 18)
        path.closeSubpath()
        return path

    def __bubble_body_rect(self, tail_side: str) -> QRectF:
        return QRectF(8, 8, self.width() - 16, self.height() - 16)

    def __draw_bubble_background(self, painter: QPainter, path: QPainterPath) -> None:
        config = self.__visual_config()
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(config["fill"]))
        painter.drawPath(path)
        painter.restore()

    def __draw_hatch_pattern(self, painter: QPainter, path: QPainterPath) -> None:
        config = self.__visual_config()
        return

    def __draw_bubble_outline(self, painter: QPainter, path: QPainterPath) -> None:
        config = self.__visual_config()
        painter.save()
        pen = QPen(QColor(config["outline"]), self.__outline_width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        painter.restore()

    def __draw_message_text(self, painter: QPainter) -> None:
        config = self.__visual_config()
        font, text_rect, wrapped_message = self.__fit_text_to_bubble()

        painter.save()
        painter.setPen(QColor(config["text"]))
        painter.setFont(font)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignTop, wrapped_message)
        painter.restore()

        self.__draw_message_date(painter)

    def __message_font(self, point_size: Optional[int] = None) -> QFont:
        font = QFont("Segoe UI", point_size or self.__max_font_size)
        font.setWeight(QFont.Weight.DemiBold)
        return font

    def __text_padding(self) -> dict[str, int]:
        config = self.__visual_config()

        if config["tail_side"] == "left":
            return {
                "left": 30,
                "top": 25,
                "right": 30,
                "bottom": 42,
            }

        return {
            "left": 30,
            "top": 25,
            "right": 30,
            "bottom": 42,
        }

    def __text_rect(self) -> QRectF:
        padding = self.__text_padding()

        return QRectF(
            padding["left"],
            padding["top"],
            self.width() - padding["left"] - padding["right"],
            self.height() - padding["top"] - padding["bottom"],
        )

    def __fit_text_to_bubble(self) -> tuple[QFont, QRectF, str]:
        text_rect = self.__text_rect()

        for point_size in range(self.__max_font_size, self.__min_font_size - 1, -1):
            font = self.__message_font(point_size)
            metrics = QFontMetrics(font)
            wrapped_message = self.__wrap_text_for_width(metrics, int(text_rect.width()))
            measured = metrics.boundingRect(
                0,
                0,
                int(text_rect.width()),
                1000,
                Qt.TextWordWrap,
                wrapped_message,
            )

            if measured.height() <= text_rect.height() and measured.width() <= text_rect.width():
                return font, text_rect, wrapped_message

        font = self.__message_font(self.__min_font_size)
        metrics = QFontMetrics(font)
        return font, text_rect, self.__wrap_text_for_width(metrics, int(text_rect.width()))

    def __draw_message_date(self, painter: QPainter) -> None:
        if not self.__date:
            return

        config = self.__visual_config()
        date_font = QFont("Segoe UI", 8)
        date_font.setWeight(QFont.Weight.Medium)
        metrics = QFontMetrics(date_font)
        date_rect = self.__date_rect(metrics.horizontalAdvance(self.__date), metrics.height())

        painter.save()
        painter.setPen(QColor(config["text"]))
        painter.setFont(date_font)
        painter.drawText(date_rect, Qt.AlignRight | Qt.AlignVCenter, self.__date)
        painter.restore()

    def __date_rect(self, date_width: int, date_height: int) -> QRectF:
        padding = self.__text_padding()
        right = self.width() - padding["right"]
        bottom = self.height() - 14
        left = max(padding["left"], right - max(90, date_width))
        top = max(padding["top"], bottom - max(date_height, 14))

        return QRectF(left, top, right - left, bottom - top)

    def __wrap_text_for_width(self, metrics: QFontMetrics, max_width: int) -> str:
        paragraphs = self.__message.splitlines() or [self.__message]
        wrapped_paragraphs = []

        for paragraph in paragraphs:
            wrapped_paragraphs.extend(self.__wrap_paragraph(paragraph, metrics, max_width))

        return "\n".join(wrapped_paragraphs)

    def __wrap_paragraph(self, paragraph: str, metrics: QFontMetrics, max_width: int) -> list[str]:
        if not paragraph:
            return [""]

        lines = []
        current_line = ""

        for word in paragraph.split(" "):
            candidate = word if not current_line else f"{current_line} {word}"

            if metrics.horizontalAdvance(candidate) <= max_width:
                current_line = candidate
                continue

            if current_line:
                lines.append(current_line)
                current_line = ""

            if metrics.horizontalAdvance(word) <= max_width:
                current_line = word
            else:
                broken_word_lines = self.__break_word(word, metrics, max_width)
                lines.extend(broken_word_lines[:-1])
                current_line = broken_word_lines[-1] if broken_word_lines else ""

        if current_line:
            lines.append(current_line)

        return lines

    def __break_word(self, word: str, metrics: QFontMetrics, max_width: int) -> list[str]:
        parts = []
        current_part = ""

        for character in word:
            candidate = f"{current_part}{character}"

            if metrics.horizontalAdvance(candidate) <= max_width:
                current_part = candidate
                continue

            if current_part:
                parts.append(current_part)

            current_part = character

        if current_part:
            parts.append(current_part)

        return parts

    def __text_flags(self):
        flags = Qt.TextWordWrap
        wrap_anywhere = getattr(Qt, "TextWrapAnywhere", None)

        if wrap_anywhere is not None:
            flags |= wrap_anywhere

        return flags

    def __fit_bubble_to_text(self) -> None:
        padding = self.__text_padding()
        metrics = QFontMetrics(self.__message_font(self.__max_font_size))

        wrapped_for_max = self.__wrap_text_for_width(metrics, self.__max_text_width)
        single_line_rect = metrics.boundingRect(0, 0, self.__max_text_width, 1000, Qt.TextWordWrap, wrapped_for_max)
        width = min(
            max(single_line_rect.width() + padding["left"] + padding["right"], self.__min_bubble_width),
            self.__max_bubble_width,
        )

        inner_width = width - padding["left"] - padding["right"]
        text_rect = metrics.boundingRect(
            0,
            0,
            inner_width,
            1000,
            Qt.TextWordWrap,
            self.__wrap_text_for_width(metrics, inner_width),
        )
        height = max(text_rect.height() + padding["top"] + padding["bottom"], self.__min_bubble_height)

        while width < self.__max_bubble_width and text_rect.height() > self.__target_text_height(height, padding):
            width = min(width + 24, self.__max_bubble_width)
            inner_width = width - padding["left"] - padding["right"]
            wrapped_text = self.__wrap_text_for_width(metrics, inner_width)
            text_rect = metrics.boundingRect(0, 0, inner_width, 1000, Qt.TextWordWrap, wrapped_text)
            height = max(text_rect.height() + padding["top"] + padding["bottom"], self.__min_bubble_height)

        self.setFixedSize(width, height)
        self.updateGeometry()
        self.update()

    def __target_text_height(self, bubble_height: int, padding: dict[str, int]) -> int:
        return bubble_height - padding["top"] - padding["bottom"]


class CloudMessageInput(QFrame):
    """Rounded message input painted with QPainter."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__border_color = QColor("#D66EF2")
        self.__accent_color = QColor("#D66EF2")
        self.__cloud_fill = QColor("#F6BBD0")
        self.__min_cloud_height = 96
        self.__max_cloud_height = 360
        self.__horizontal_padding = 42
        self.__top_padding = 34
        self.__bottom_padding = 28

        self.setObjectName("cloudMessageInput")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumHeight(self.__min_cloud_height)

        self.__text_edit = QTextEdit(self)
        self.__text_edit.setObjectName("cloudInputText")
        self.__text_edit.setPlaceholderText("Type your message here")
        self.__text_edit.setFrameShape(QFrame.NoFrame)
        self.__text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.__text_edit.textChanged.connect(self.__fit_cloud_to_text)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.__cloud_text_margins())
        layout.setSpacing(0)
        layout.addWidget(self.__text_edit, alignment=Qt.AlignVCenter)
        self.__layout = layout
        self.setFixedHeight(self.__min_cloud_height)

    # Functional methods.
    def text_edit(self) -> QTextEdit:
        return self.__text_edit

    def toPlainText(self) -> str:
        return self.__text_edit.toPlainText()

    def clear(self) -> None:
        self.__text_edit.clear()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.__fit_cloud_to_text()

    # Visual methods.
    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = self.__build_cloud_path()

        self.__draw_cloud_fill(painter, path)
        self.__draw_cloud_outline(painter, path)
        self.__draw_accent_strokes(painter)

    def __build_cloud_path(self) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(8, 8, self.width() - 16, self.height() - 16), 18, 18)
        path.closeSubpath()
        return path

    def __draw_cloud_fill(self, painter: QPainter, path: QPainterPath) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__cloud_fill)
        painter.drawPath(path)
        painter.restore()

    def __draw_cloud_outline(self, painter: QPainter, path: QPainterPath) -> None:
        painter.save()
        pen = QPen(self.__border_color, 5)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        painter.restore()

    def __draw_accent_strokes(self, painter: QPainter) -> None:
        return

    def __fit_cloud_to_text(self) -> None:
        text_width = max(120, self.width() - self.__horizontal_padding * 2)
        document = self.__text_edit.document()
        document.setTextWidth(text_width)

        text_height = max(24, int(document.size().height()) + 8)
        target_height = min(
            max(text_height + self.__top_padding + self.__bottom_padding, self.__min_cloud_height),
            self.__max_cloud_height,
        )

        if self.height() != target_height:
            self.setFixedHeight(target_height)
            self.updateGeometry()

        available_height = max(24, target_height - self.__top_padding - self.__bottom_padding)
        top_margin = self.__top_padding + max(0, (available_height - text_height) // 2)
        vertical_offset = max(0, (available_height - text_height) // 2)
        top_margin = self.__top_padding + vertical_offset
        bottom_margin = self.__bottom_padding + max(0, (available_height - text_height) - vertical_offset)

        self.__layout.setContentsMargins(
            self.__horizontal_padding,
            top_margin,
            self.__horizontal_padding,
            bottom_margin,
        )
        self.update()

    def __cloud_text_margins(self) -> tuple[int, int, int, int]:
        return (
            self.__horizontal_padding,
            self.__top_padding,
            self.__horizontal_padding,
            self.__bottom_padding,
        )


class ChatView(View):
    def __init__(self, window: QMainWindow):
        super().__init__(window, key="chat", title="Chat")
        self.auth = Autorizacion()
        self.chat = Chat()
        self.modelo_ia = ModeloIA()
        self.main_window.resize(CHAT_CANVAS_WIDTH + 180, CHAT_CANVAS_HEIGHT + 160)
        self.main_window.setMinimumSize(1100, 720)
        self.build_ui()

    def build_ui(self) -> None:
        self.root = QVBoxLayout()
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(0)

        self.__apply_chat_styles()

        shell = QFrame()
        shell.setObjectName("chatShell")
        shell.setFixedSize(CHAT_CANVAS_WIDTH + 46, CHAT_CANVAS_HEIGHT + 46)

        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(23, 23, 23, 23)
        shell_layout.setSpacing(0)

        background = QFrame()
        background.setObjectName("chatBackground")
        background.setFixedSize(CHAT_CANVAS_WIDTH, CHAT_CANVAS_HEIGHT)

        title = GradientTitleLabel("Dino workspace", background)
        title.setObjectName("chatTitle")
        title.setAlignment(Qt.AlignCenter)

        shell_layout.addWidget(background)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("chatScrollArea")
        scroll_area.setWidgetResizable(False)
        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setWidget(shell)
        self.root.addWidget(scroll_area)

        self.agregar_widget("chat_shell", shell)
        self.agregar_widget("chat_scroll_area", scroll_area)
        self.agregar_widget("chat_background", background)
        self.agregar_widget("chat_title", title)

        self.__build_decorations(background)
        self.__build_messages_area(background)
        self.__build_input_area(background)
        self.__position_header()
        self.__position_decorations()
        self.__position_functional_elements()

    def __build_decorations(self, background: QFrame) -> None:
        confetti_layer = ConfettiLayer(background)
        confetti_layer.setFixedSize(CHAT_CANVAS_WIDTH, CHAT_CANVAS_HEIGHT)

        panel_frame = DecorativePanelFrame(background)
        panel_frame.setFixedSize(CHAT_CANVAS_WIDTH, CHAT_CANVAS_HEIGHT)

        self.agregar_widget("confetti_layer", confetti_layer)
        self.agregar_widget("panel_frame", panel_frame)

        self.__build_image(background, "title_red_ghost_image", RED_GHOST_IMAGE, 62, 52)
        self.__build_image(background, "title_cactus_image", CACTUS_PACMAN_IMAGE, 115, 84)
        self.__build_image(background, "title_grass_image", YELLOW_GRASS_IMAGE, 430, 56)

    def __build_image(
        self,
        parent: QWidget,
        key: str,
        file_name: str,
        width: int,
        height: int,
    ) -> QLabel:
        image = QLabel(parent)
        image.setObjectName(key)
        image.setFixedSize(width, height)
        image.setScaledContents(True)
        image.setPixmap(QPixmap(str(ASSETS_DIR / file_name)))

        self.agregar_widget(key, image)
        return image

    def __build_messages_area(self, background: QFrame) -> None:
        conversation_area = QScrollArea(background)
        conversation_area.setObjectName("conversationArea")
        conversation_area.setWidgetResizable(True)
        conversation_area.setFrameShape(QFrame.NoFrame)

        messages_container = QWidget()
        messages_container.setObjectName("messagesContainer")

        messages_layout = QVBoxLayout(messages_container)
        messages_layout.setContentsMargins(24, 18, 24, 18)
        messages_layout.setSpacing(12)
        messages_layout.addStretch(1)

        conversation_area.setWidget(messages_container)

        self.agregar_widget("conversation_area", conversation_area)
        self.agregar_widget("messages_container", messages_container)
        self.widgets["messages_layout"] = messages_layout

    def __build_input_area(self, background: QFrame) -> None:
        message_input = CloudMessageInput(background)

        send_button = QPushButton("Send", background)
        send_button.setObjectName("sendButton")
        send_button.clicked.connect(self.__send_message)

        action_panel = QFrame(background)
        action_panel.setObjectName("chatActionPanel")

        upload_button = QPushButton("Upload Files", action_panel)
        upload_button.setObjectName("uploadFilesButton")
        upload_button.clicked.connect(self.__upload_file)

        export_button = QPushButton("Export conversations", action_panel)
        export_button.setObjectName("exportConversationsButton")
        export_button.clicked.connect(self.__export_conversation)

        self.agregar_widget("message_input", message_input)
        self.agregar_widget("send_button", send_button)
        self.agregar_widget("action_panel", action_panel)
        self.agregar_widget("upload_button", upload_button)
        self.agregar_widget("export_button", export_button)

    def __position_header(self) -> None:
        self.widgets["chat_title"].setFixedSize(720, 86)
        self.widgets["chat_title"].move(365, 22)

        self.widgets["chat_title"].raise_()

    def __position_decorations(self) -> None:
        self.widgets["confetti_layer"].move(0, 0)
        self.widgets["confetti_layer"].raise_()

        self.widgets["panel_frame"].move(0, 0)
        self.widgets["panel_frame"].raise_()

        title_red_ghost = self.widgets["title_red_ghost_image"]
        title_red_ghost.move(998, 42)

        title_cactus = self.widgets["title_cactus_image"]
        title_cactus.move(1055, 28)

        title_grass = self.widgets["title_grass_image"]
        title_grass.move(505, 94)

        for key in ("title_red_ghost_image", "title_cactus_image", "title_grass_image"):
            self.widgets[key].raise_()

        self.widgets["chat_title"].raise_()

    def __position_functional_elements(self) -> None:
        self.widgets["conversation_area"].setGeometry(105, 155, 1245, 360)
        self.widgets["message_input"].setGeometry(330, 555, 780, 104)
        self.widgets["send_button"].setGeometry(620, 674, 220, 42)
        self.widgets["action_panel"].setGeometry(65, 530, 230, 155)
        self.widgets["upload_button"].setGeometry(40, 28, 150, 44)
        self.widgets["export_button"].setGeometry(28, 92, 174, 44)

        for key in (
            "conversation_area",
            "message_input",
            "send_button",
            "action_panel",
        ):
            self.widgets[key].raise_()

        self.widgets["upload_button"].raise_()
        self.widgets["export_button"].raise_()

    def __add_message_bubble(self, message: str, sender: str, date: Optional[str] = None) -> MessageBubble:
        layout = self.widgets["messages_layout"]
        bubble = MessageBubble(message=message, sender=sender, date=date)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(14)

        icon = QLabel()
        icon.setFixedSize(58, 58)
        icon.setScaledContents(True)
        icon_file = BLUE_GHOST_IMAGE if sender == "bot" else DINO_PURPLE_IMAGE
        icon.setPixmap(QPixmap(str(ASSETS_DIR / icon_file)))

        if sender == "usuario":
            row.addStretch(1)
            row.addWidget(bubble)
            row.addWidget(icon)
        else:
            row.addWidget(icon)
            row.addWidget(bubble)
            row.addStretch(1)

        layout.insertLayout(max(0, layout.count() - 1), row)
        self.__scroll_to_bottom()
        return bubble

    def __send_message(self) -> None:
        message_input = self.widgets["message_input"]
        message = message_input.toPlainText().strip()

        if not message:
            return

        self.chat.conversacion.agregar_mensaje(message, "usuario")
        self.__add_message_bubble(message, "usuario")
        respuesta = self.modelo_ia.procesar_pregunta(message, self.chat.conversacion)
        self.chat.conversacion.agregar_mensaje(respuesta, "bot")
        message_input.clear()
        self.__add_message_bubble(respuesta, "bot")

    def __upload_file(self) -> None:
        filters = f"Archivos permitidos ({" ".join(f"*{ext}" for ext in ManejadorArchivo.tipo_archivo_permitido)})"
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Seleccionar archivo",
            "",
            filters,
        )

        if not file_path:
            return
        
        self.__add_file_to_conversation(file_path)
    
    def __add_file_to_conversation(self, file_path: str) -> None:
        # TODO: Crear método para solicitar confirmación del usuario si desea reemplazar el archivo
        try:
            usuario = self.auth.usuario_actual
            if not usuario:
                raise Exception("No se ha autenticado ningún usuario. Por favor, inicie sesión para cargar archivos.")
            archivo: Archivo = ManejadorArchivo.obtener_informacion_archivo(file_path, id_user=usuario.id)
            self.chat.conversacion.agregar_archivo(archivo)

            self.main_window.loaded_file_name = archivo.nombre
            self.__add_message_bubble(f"Archivo cargado: {archivo.nombre}", "bot")
        except Exception as e:
            print(f"Error al cargar el archivo: {str(e)}")
            self.__add_message_bubble(f"Error al cargar el archivo: {str(e)}", "bot")

    def __export_conversation(self) -> None:
        self.__add_message_bubble("Exportacion de conversacion preparada.", "bot")

    def __scroll_to_bottom(self) -> None:
        scroll_bar = self.widgets["conversation_area"].verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def __apply_chat_styles(self) -> None:
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: #4AAFEF;
                font-family: Segoe UI, Arial, sans-serif;
            }

            QWidget#root {
                background-color: #4AAFEF;
            }

            QFrame#chatShell {
                border-radius: 30px;
                background-color: #4AAFEF;
            }

            QFrame#chatBackground {
                background-color: #A9F0B8;
                border: none;
                border-radius: 24px;
            }

            QLabel#chatTitle {
                background-color: transparent;
            }

            QScrollArea#conversationArea {
                background-color: rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(126, 77, 255, 0.8);
                border-radius: 18px;
            }

            QScrollArea#conversationArea QScrollBar:vertical {
                background-color: transparent;
                width: 22px;
                margin: 20px 0px 20px 0px;
            }

            QScrollArea#conversationArea QScrollBar::handle:vertical {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #7AF7E1,
                    stop: 0.35 #6B57FF,
                    stop: 0.70 #F38BDA,
                    stop: 1 #5DEFE0
                );
                border-radius: 10px;
                min-height: 92px;
            }

            QScrollArea#conversationArea QScrollBar::add-line:vertical,
            QScrollArea#conversationArea QScrollBar::sub-line:vertical {
                background-color: transparent;
                border: none;
                height: 18px;
            }

            QScrollArea#conversationArea QScrollBar::up-arrow:vertical {
                image: none;
                width: 0px;
                height: 0px;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-bottom: 9px solid #6B57FF;
            }

            QScrollArea#conversationArea QScrollBar::down-arrow:vertical {
                image: none;
                width: 0px;
                height: 0px;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 9px solid #F38BDA;
            }

            QScrollArea#conversationArea QScrollBar::add-page:vertical,
            QScrollArea#conversationArea QScrollBar::sub-page:vertical {
                background-color: transparent;
            }

            QScrollArea#conversationArea > QWidget {
                background-color: transparent;
            }

            QWidget#messagesContainer {
                background-color: transparent;
            }

            QTextEdit#messageInput {
                background-color: #FFFFFF;
                border: 3px solid #8ACFE8;
                border-radius: 0px;
                color: #2F2F2F;
                font-size: 13px;
                font-weight: 700;
                padding: 8px;
            }

            QTextEdit#cloudInputText {
                background-color: transparent;
                border: none;
                color: #2F2F2F;
                font-size: 13px;
                font-weight: 700;
            }

            QTextEdit#cloudInputText::placeholder {
                color: #8B8B8B;
            }

            QPushButton#sendButton {
                background-color: #FFD23F;
                border: 4px solid #E98600;
                border-radius: 18px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 900;
                min-height: 42px;
            }

            QPushButton#sendButton:hover {
                background-color: #FFE073;
            }

            QPushButton#sendButton:pressed {
                background-color: #F1BE23;
            }

            QFrame#chatActionPanel {
                background: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #7AF7E1,
                    stop: 0.35 #CDBBFF,
                    stop: 0.70 #F6BBD0,
                    stop: 1 #8FEFD6
                );
                border: 4px dashed #7E4DFF;
                border-radius: 26px;
            }

            QPushButton#uploadFilesButton {
                background-color: #FFE873;
                border: 5px solid #D66EF2;
                border-radius: 13px;
                color: #2F2F2F;
                font-size: 12px;
                font-weight: 900;
            }

            QPushButton#uploadFilesButton:hover {
                background-color: #FFF09A;
            }

            QPushButton#exportConversationsButton {
                background-color: #FFFFFF;
                border: 5px solid #FF7EAA;
                border-radius: 13px;
                color: #2F2F2F;
                font-size: 12px;
                font-weight: 900;
            }

            QPushButton#exportConversationsButton:hover {
                background-color: #FFF0F6;
            }

            """
        )

    # Método para invocar cuando se muestra la vista
    def on_show(self) -> None:
        super().on_show()
        try:
            # Obtenemos los mensajes previos
            mensajes_previos = self.chat.obtener_ultimos_mensajes()
            for mensaje in mensajes_previos:
                self.__add_message_bubble(message=mensaje.contenido, sender=mensaje.emisor, date=mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S"))

            self.__scroll_to_bottom()
        except Exception as e:
            print(f"Error al cargar mensajes previos: {str(e)}")