from PySide6.QtWidgets import QMainWindow, QTabWidget, QMenuBar
from canvas.canvas_view import Canvas
from editor.text_editor import CodeEditor
from toolbar.main_toolbar import MainToolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulink-style Editor")
        self.resize(1000, 700)

        # Menu
        menubar = QMenuBar()
        file_menu = menubar.addMenu("File")
        self.setMenuBar(menubar)

        # Toolbar
        self.toolbar = MainToolbar(self)
        self.addToolBar(self.toolbar)

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Canvas tab
        self.canvas_tab = Canvas()
        self.tabs.addTab(self.canvas_tab, "Canvas")

        # Text editor tab
        self.text_tab = CodeEditor()
        self.tabs.addTab(self.text_tab, "Text Editor")