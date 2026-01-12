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

        # Group toggle buttons

        self.addSeparator()

        # Example dropdown
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        self.addWidget(combo)
