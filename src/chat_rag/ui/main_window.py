import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt

from chat_rag.ui.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chat RAG")
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

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(16)
        root.setLayout(main_layout)

        main_layout.addWidget(self._create_sidebar())
        main_layout.addWidget(self._create_chat_panel(), stretch=1)

    def _create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(14)

        title = QLabel("Chat RAG")
        title.setObjectName("appTitle")

        description = QLabel("Panel de trabajo")
        description.setObjectName("sideText")

        file_section = QLabel("Archivo cargado")
        file_section.setObjectName("sideSection")

        self.file_name_label = QLabel("Sin archivo seleccionado")
        self.file_name_label.setObjectName("fileName")
        self.file_name_label.setWordWrap(True)

        load_button = QPushButton("Cargar archivo")
        load_button.setObjectName("sideButton")
        load_button.clicked.connect(self._select_file)

        export_json_button = QPushButton("Exportar JSON")
        export_json_button.setObjectName("sideButton")
        export_json_button.clicked.connect(self._show_pending_action)

        export_xml_button = QPushButton("Exportar XML")
        export_xml_button.setObjectName("sideButton")
        export_xml_button.clicked.connect(self._show_pending_action)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(18)
        layout.addWidget(file_section)
        layout.addWidget(self.file_name_label)
        layout.addWidget(load_button)
        layout.addSpacing(8)
        layout.addWidget(export_json_button)
        layout.addWidget(export_xml_button)
        layout.addStretch()

        footer = QLabel("Vista visual inicial")
        footer.setObjectName("sideText")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        return sidebar

    def _create_chat_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("chatPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        title = QLabel("Conversacion")
        title.setObjectName("chatTitle")

        subtitle = QLabel("Realiza preguntas sobre el archivo seleccionado")
        subtitle.setObjectName("chatSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        conversation_body = QWidget()
        conversation_body.setObjectName("conversationBody")
        self.messages_layout = QVBoxLayout(conversation_body)
        self.messages_layout.setContentsMargins(16, 16, 16, 16)
        self.messages_layout.setSpacing(10)
        self.messages_layout.addStretch()

        self.scroll_area.setWidget(conversation_body)
        layout.addWidget(self.scroll_area, stretch=1)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.message_input = QTextEdit()
        self.message_input.setObjectName("messageInput")
        self.message_input.setPlaceholderText("Escribe tu pregunta...")
        self.message_input.setFixedHeight(70)

        send_button = QPushButton("Enviar")
        send_button.setObjectName("sendButton")
        send_button.setFixedHeight(70)
        send_button.clicked.connect(self._send_message)

        input_row.addWidget(self.message_input, stretch=1)
        input_row.addWidget(send_button)
        layout.addLayout(input_row)

        self._add_message(
            "system",
            "Bienvenida. Carga un archivo y escribe una pregunta para iniciar la conversacion.",
        )

        return panel

    def _add_message(self, sender: str, text: str) -> None:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(560)

        if sender == "user":
            bubble.setObjectName("userBubble")
            row.addStretch()
            row.addWidget(bubble)
        else:
            bubble.setObjectName("systemBubble")
            row.addWidget(bubble)
            row.addStretch()

        self.messages_layout.insertLayout(self.messages_layout.count() - 1, row)
        self._scroll_to_bottom()

    def _send_message(self) -> None:
        message = self.message_input.toPlainText().strip()
        if not message:
            return

        self._add_message("user", message)
        self.message_input.clear()

        if self.loaded_file_name:
            response = (
                "Respuesta simulada con base en el archivo cargado: "
                f"{self.loaded_file_name}."
            )
        else:
            response = "Para responder sobre un documento, primero carga un archivo."

        self._add_message("system", response)

    def _select_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos permitidos (*.txt *.pdf *.json *.xml)",
        )

        if not file_path:
            return

        self.loaded_file_name = file_path.split("/")[-1]
        self.file_name_label.setText(self.loaded_file_name)
        self._add_message("system", f"Archivo cargado: {self.loaded_file_name}")

    def _show_pending_action(self) -> None:
        QMessageBox.information(
            self,
            "Accion pendiente",
            "Esta opcion visual queda lista para conectarse al servicio correspondiente.",
        )

    def _scroll_to_bottom(self) -> None:
        bar = self.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

def run_app() -> None:
    app = QApplication(sys.argv)
    login = LoginDialog()

    if login.exec() == LoginDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    sys.exit(0)
