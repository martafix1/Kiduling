from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QBrush, QColor

class BlockItem(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setBrush(QBrush(QColor("lightgray")))
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)