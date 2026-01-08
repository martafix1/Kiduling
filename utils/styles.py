
from PySide6.QtWidgets import QMenu


def create_menu() -> QMenu:
    menu = QMenu()
    menu.setStyleSheet("""
        QMenu {
            background-color: #f0f0f0;
            border: 1px solid #aaa;
            border-radius: 0px;
        }
        QMenu::item:selected {
            background-color: #3874f2;
            color: white;
        }
    """)
    return menu