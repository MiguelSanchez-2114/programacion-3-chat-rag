import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chat RAG")
        self.resize(980, 680)

        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout()
        root.setLayout(main_layout)

        # Texto de referencia.
        workarea_label = QLabel("Área de trabajo")
        workarea_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        workarea_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(workarea_label)

def run_app() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
