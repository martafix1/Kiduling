from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from .block_item import BlockItem

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        # Example block
        block = BlockItem(0, 0, 120, 60)
        self.scene().addItem(block)

    def wheelEvent(self, event):
        zoom = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom, zoom)