# base_items.py

from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QMenu,
)
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtCore import Qt

from .canvas_graph import GraphNode, BlockNode, CornerNode, GraphEdge


def show_delete_menu(event, delete_callback):
    menu = QMenu()
    menu.addAction("Delete", delete_callback)
    menu.exec(event.screenPos())

def update_node_position(item):
    item.node.x = item.scenePos().x()
    item.node.y = item.scenePos().y()



# class NodeItem(QGraphicsItem):
#     """
#     Base Qt item for all graph nodes (blocks, corners).
#     """

#     def __init__(self, node: GraphNode, canvas):
#         super().__init__()
#         self.node = node
#         self.canvas = canvas  # reference to owning canvas

#         self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

#         self.setPos(node.x, node.y)

#     # ---- interaction ----

#     def mouseMoveEvent(self, event):
#         super().mouseMoveEvent(event)

#         # update graph position
#         self.node.x = self.scenePos().x()
#         self.node.y = self.scenePos().y()

#         # update connected edges
#         for edge in self.node.edges:
#             if hasattr(edge, "_item"):
#                 edge._item.update_position()

#     def contextMenuEvent(self, event):
#         show_delete_menu(event, self._delete_self)

#     def _delete_self(self):
#         self.canvas.delete_node(self.node)


class BlockItem(QGraphicsRectItem):
    def __init__(self, node: BlockNode, canvas):
        w = node.properties["width"]
        h = node.properties["height"]

        QGraphicsRectItem.__init__(self, 0, 0, w, h)
        
        self.node = node
        self.canvas = canvas  # reference to owning canvas

        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        self.setPos(node.x, node.y)

        self.setBrush(QBrush(QColor("lightgray")))

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction("Delete", lambda: self.canvas.delete_node(self.node))
        menu.addAction("Connect", lambda: self.canvas.start_connection(self.node, event.scenePos()))
        menu.exec(event.screenPos())
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # update graph position
        self.node.x = self.scenePos().x()
        self.node.y = self.scenePos().y()
        for edge in self.node.edges:
            edge._item.update_position()



class CornerItem(QGraphicsEllipseItem):
    def __init__(self, node: CornerNode, canvas):
        r = 6
        QGraphicsEllipseItem.__init__(self, -r, -r, 2 * r, 2 * r)
       
        self.node = node
        self.canvas = canvas  # reference to owning canvas

        self.setFlag(self.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        self.setPos(node.x, node.y)

        self.setBrush(QBrush(QColor("darkgray")))
    
    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction("Delete", lambda: self.canvas.delete_node(self.node))
        menu.exec(event.screenPos())

class ConnectionItem(QGraphicsLineItem):
    """
    Qt item for graph edges (pipes, wires).
    """

    def __init__(self, edge: GraphEdge, canvas):
        super().__init__()
        self.edge = edge
        self.canvas = canvas

        # back-reference for updates
        edge._item = self

        self.setPen(QPen(QColor("black"), 2))
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        self.update_position()

    def update_position(self):
        a = self.edge.a
        b = self.edge.b
        self.setLine(a.x, a.y, b.x, b.y)

    def contextMenuEvent(self, event):
        show_delete_menu(event, self._delete_self)

    def _delete_self(self):
        self.canvas.delete_edge(self.edge)



