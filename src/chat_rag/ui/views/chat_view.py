from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from chat_rag.ui.views.view import View


class ChatView(View):
    def __init__(self, window: QMainWindow):
        super().__init__(window, key="chat", title="Chat")
        self.build_ui()

    def build_ui(self) -> None:
        self.root = QVBoxLayout()
        self.root.setContentsMargins(18, 18, 18, 18)
        self.root.setSpacing(14)

        chat_panel = QFrame()
        chat_panel.setObjectName("chatPanel")

        panel_layout = QVBoxLayout(chat_panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(12)

        title = QLabel("DiNO Chat RAG")
        title.setObjectName("chatTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Chat view loaded successfully")
        subtitle.setObjectName("chatSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        conversation_area = QTextEdit()
        conversation_area.setObjectName("messageInput")
        conversation_area.setPlaceholderText("Conversation area")
        conversation_area.setReadOnly(True)

        message_input = QTextEdit()
        message_input.setObjectName("messageInput")
        message_input.setPlaceholderText("Type your message here")
        message_input.setFixedHeight(90)

        send_button = QPushButton("Send")
        send_button.setObjectName("sendButton")

        panel_layout.addWidget(title)
        panel_layout.addWidget(subtitle)
        panel_layout.addWidget(conversation_area, stretch=1)
        panel_layout.addWidget(message_input)
        panel_layout.addWidget(send_button)

        self.root.addWidget(chat_panel)

        self.agregar_widget("chat_panel", chat_panel)
        self.agregar_widget("chat_title", title)
        self.agregar_widget("chat_subtitle", subtitle)
        self.agregar_widget("conversation_area", conversation_area)
        self.agregar_widget("message_input", message_input)
        self.agregar_widget("send_button", send_button)
