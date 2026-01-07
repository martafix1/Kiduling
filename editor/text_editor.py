from PySide6.QtWidgets import QPlainTextEdit

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Write Python code here...")