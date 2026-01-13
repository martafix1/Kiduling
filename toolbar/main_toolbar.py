from PySide6.QtWidgets import QToolBar, QComboBox
from PySide6.QtGui import QIcon, QAction

class MainToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)
        self.setMovable(False)

        # Example button: New Block
        new_block_action = QAction(QIcon("resources/icons/speedometer-arrow.svg"), "New Block", self)
        self.addAction(new_block_action)

        self.debug_action = QAction(QIcon("resources/icons/bug-slash.svg"), "Debug", self)
        self.addAction(self.debug_action)

        # Example toggle button: Select/Draw Mode
        select_action = QAction(QIcon("resources/icons/select.png"), "Select Mode", self)
        select_action.setCheckable(True)
        self.addAction(select_action)

        draw_action = QAction(QIcon("resources/icons/draw.png"), "Draw Mode", self)
        draw_action.setCheckable(True)
        self.addAction(draw_action)

        self.addSeparator()

        canvas_sceneResizable_action = QAction(QIcon(),"scene resizable",self)
        canvas_sceneResizable_action.setCheckable(True)
        canvas_sceneResizable_action.setChecked(True)
        #canvas_sceneResizable_action.connect(lambda: parent.canvas_tab.updateProperty("scene_resizable",canvas_sceneResizable_action.isChecked()))
        canvas_sceneResizable_action.toggled.connect(
            lambda checked: parent.canvas_tab.updateProperty("scene_resizable", checked)
            )
        self.addAction(canvas_sceneResizable_action)
        # Group toggle buttons

        self.addSeparator()

        # Example dropdown
        combo = QComboBox()
        combo.addItems(["Grid background", "Pixelmap grid background", "White"])
        self.addWidget(combo)

        combo.currentIndexChanged.connect(lambda index: parent.canvas_tab.updateProperty("canvas_background", index))
