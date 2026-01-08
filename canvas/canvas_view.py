from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

from utils import styles
from .canvas_graph import CanvasGraph, BlockNode, CornerNode, GraphEdge
from .base_items import BlockItem, CornerItem, EdgeItem


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        # ✅ Document model
        self.graph = CanvasGraph()

        # used by context menu
        self._rc_scene_pos = None

    def wheelEvent(self, event):
        zoom = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom, zoom)

    def contextMenuEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        self._rc_scene_pos = scene_pos

        # If user clicked on an item, let the item handle it
        items = self.scene().items(scene_pos)
        if items:
            return

        # Empty canvas → show add menu
        menu = styles.create_menu()
        add_menu = menu.addMenu("Add")

        add_block_action = add_menu.addAction("Block")
        add_corner_action = add_menu.addAction("Corner")

        add_block_action.triggered.connect(self._add_block_from_menu)
        add_corner_action.triggered.connect(self._add_corner_from_menu)

        menu.exec(event.globalPos())



    def add_block(self, x, y):
        node = BlockNode(x, y)
        self.graph.add_node(node)

        item = BlockItem(node, self)
        self.scene().addItem(item)


    def add_corner(self, x, y):
        node = CornerNode(x, y)
        self.graph.add_node(node)

        item = CornerItem(node, self)
        self.scene().addItem(item)



    def delete_node(self, node):
        # remove connected edges first
        for edge in node.edges[:]:
            self.delete_edge(edge)

        # remove graph node
        self.graph.remove_node(node)

        # remove corresponding Qt item
        for item in self.scene().items():
            if hasattr(item, "node") and item.node is node:
                self.scene().removeItem(item)
                break
    

    def delete_edge(self, edge):
        self.graph.remove_edge(edge)

        for item in self.scene().items():
            if hasattr(item, "edge") and item.edge is edge:
                self.scene().removeItem(item)
                break



    # context menu API
    def _add_block_from_menu(self):
        if self._rc_scene_pos is None:
            return
        self.add_block(self._rc_scene_pos.x(), self._rc_scene_pos.y())

    def _add_corner_from_menu(self):
        if self._rc_scene_pos is None:
            return
        self.add_corner(self._rc_scene_pos.x(), self._rc_scene_pos.y())


    

