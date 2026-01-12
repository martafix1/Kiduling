from PySide6.QtWidgets import QMainWindow, QTabWidget, QMenuBar
from canvas.canvas_view import Canvas
from editor.text_editor import CodeEditor
from toolbar.main_toolbar import MainToolbar
from canvas.canvas_graph import GraphNode, GraphEdge


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

        # Connect toolbar actions
        self.toolbar.debug_action.triggered.connect(self.print_cavas_graphInfo)

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Canvas tab
        self.canvas_tab = Canvas()
        self.tabs.addTab(self.canvas_tab, "Canvas")

        # Text editor tab
        self.text_tab = CodeEditor()
        self.tabs.addTab(self.text_tab, "Text Editor")

    def print_cavas_graphInfo(self):
        print("Debug: All stuff from CanvasGraph - Nodes:")
        for node in self.canvas_tab.graph.nodes.values():
            print(f"Node ID:  {node.id}, Position: ({node.x}, {node.y}), Layer: {node.layer}, Properties: {node.properties}, Edges: {[e.id for e in node.edges]}")
        print("Debug: All stuff from CanvasGraph - Edges:")
        for edge in self.canvas_tab.graph.edges.values():
            print(f"Edge ID: {edge.id}, A: {edge.a}, B: {edge.b}, Layer: {edge.layer}, Properties: {edge.properties}")
        print("End debug")

