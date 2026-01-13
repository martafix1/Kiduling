from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from PySide6.QtGui import QBrush, QColor, QPen, QMouseEvent, QPixmap
from PySide6.QtCore import Qt, QRectF, QRect

from typing import Union, Dict, Any

from utils import styles
from .canvas_graph import CanvasGraph, BlockNode, CornerNode, GraphEdge
from .base_items import BlockItem, CornerItem, ConnectionItem


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        

        

        self.properties: Dict[str, Any] = {}
        self.properties["scene_resizable"] = True
        self.properties["zoom"] = 1
        self.properties["canvas_background"] = 0

        # ✅ Document model
        self.graph = CanvasGraph()

        # used by context menu
        self._rc_scene_pos = None
        
        #used for conecting
        self._current_connection = None

    def wheelEvent(self, event):
        delta_zoom = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.properties["zoom"] = self.properties["zoom"]*delta_zoom
        self.scale(delta_zoom, delta_zoom)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.viewport().setCursor(Qt.ClosedHandCursor)

            # Fake a left-button press so Qt starts dragging
            fake_event = QMouseEvent(
                event.type(),
                event.position(),
                Qt.LeftButton,
                Qt.LeftButton,
                event.modifiers(),
            )
            super().mousePressEvent(fake_event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_connection:
            line = self._current_connection["temp_line"]
            start_pos = self._current_connection["source_node"].scenePos()
            end_pos = self.mapToScene(event.pos())
            line.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
        self.ensure_prehaps_expand_scene_rect()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._current_connection and event.button() == Qt.MouseButton.LeftButton:
            items = self.scene().items(self.mapToScene(event.pos()))
            target_node_item = next((i for i in items if hasattr(i, "node")), None)

            if target_node_item and target_node_item.node != self._current_connection["source_node"]:
                # 1 Add edge to graph
                edge = GraphEdge(self._current_connection["source_node"],
                    target_node_item.node)
                self.graph.add_edge(edge)
                # 2 Create a proper ConnectionItem
                conn_item = ConnectionItem(edge,self)
                self.scene().addItem(conn_item)
            # Remove temp line
            self.scene().removeItem(self._current_connection["temp_line"])
            self._current_connection = None
        if event.button() == Qt.MiddleButton:
            # Fake left-button release
            fake_event = QMouseEvent(
                event.type(),
                event.position(),
                Qt.LeftButton,
                Qt.NoButton,
                event.modifiers(),
            )
            super().mouseReleaseEvent(fake_event)

            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag) # return back to selecting
            self.viewport().setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)
    """
    Draw scene rectangle, kinda for debugging
    """
    def drawForeground(self, painter, rect):
        painter.save() #chatgtp magic
        painter.setClipping(False)
        painter.setPen(QPen(Qt.red,2/self.properties["zoom"]) )
        painter.drawRect(self.scene().sceneRect())
        painter.restore()
        pass

    def drawBackground(self, painter, rect: Union[QRect, QRectF]):
        super().drawBackground(painter, rect)
        #grid_size = 50


        if self.properties["canvas_background"] == 0:
            grid_major_step = 100
            grid_minor_step = 20 # for current algo major must be divisible by minor

            if grid_major_step % grid_minor_step != 0:
                print("grid_major_step NOT DIVISIBLE BY grid_minor_step")

            grid_scaling_step_const = 10 # also a parameter
            if not hasattr(self, "grid_step_scaler"):
                self.grid_step_scaler = 1
            
            viewPortRect = self.mapToScene(self.viewport().rect()).boundingRect()
            biggurSize = max(viewPortRect.width(),viewPortRect.height())
            # if more than 100 major lines fit into the biggur size, increase the step_scaler accordingly
            while(biggurSize/(grid_major_step*self.grid_step_scaler) > grid_scaling_step_const*2):
                self.grid_step_scaler = self.grid_step_scaler * grid_scaling_step_const

            # if less than 1 major lines fit into the biggur size, decrease the step_scaler accordingly
            while(biggurSize/(grid_major_step*self.grid_step_scaler) < 1*2):
                self.grid_step_scaler = self.grid_step_scaler / grid_scaling_step_const

            # scale grid steps accordingly
            grid_major_step = grid_major_step*self.grid_step_scaler
            grid_minor_step = grid_minor_step*self.grid_step_scaler
            print(f"biggur {biggurSize}, self.scaler: {self.grid_step_scaler},grid_minor_step {grid_minor_step}")
            left = (rect.left()) - ((rect.left()) % grid_minor_step)
            top = (rect.top()) - ((rect.top()) % grid_minor_step)

            lines = []
            x = left
            while x < rect.right():
                lines.append((x, rect.top(), x, rect.bottom(),1))
                x += grid_minor_step

            y = top
            while y < rect.bottom():
                lines.append((rect.left(), y, rect.right(), y,2))
                y += grid_minor_step

            zoom = self.getProperty("zoom")
            for x1, y1, x2, y2, dir in lines:
                if (x1 % grid_major_step == 0 and dir == 1) or (y1 % grid_major_step == 0 and dir == 2) : # major line
                    painter.setPen(QPen(Qt.lightGray,2/zoom ))
                else:  # minor line
                    painter.setPen(QPen(Qt.lightGray,0.5/zoom))
                painter.drawLine(x1, y1, x2, y2)
            
            painter.setPen(QPen(Qt.darkRed, 2/zoom))
            painter.drawLine(0, rect.top(), 0, rect.bottom())
            painter.drawLine(rect.left(), 0, rect.right(), 0)
        elif self.properties["canvas_background"] == 1:
            pass
        else:
            pass
        


    def contextMenuEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        self._rc_scene_pos = scene_pos

        # If user clicked on an item, let the item handle it
        items = self.scene().items(scene_pos)
        if items:
            super().contextMenuEvent(event)
            return


        # Empty canvas → show add menu
        menu = styles.create_menu()
        add_menu = menu.addMenu("Add")

        add_block_action = add_menu.addAction("Block")
        add_corner_action = add_menu.addAction("Corner")

        add_block_action.triggered.connect(self._add_block_from_menu)
        add_corner_action.triggered.connect(self._add_corner_from_menu)

        menu.exec(event.globalPos())

    def getProperty(self,key: str) -> Any: 
        try:
            return self.properties[key]
        except KeyError:
            raise ValueError(f"Property '{key}' not found")



    def updateProperty(self,key: str ,value : Any):
        if key in self.properties:
            self.properties[key] = value
            self.resolve_genericPropertyUpdate(key,value)
        else:
            raise ValueError(f"Property '{key}' not found")


    def resolve_genericPropertyUpdate(self,key: str ,value : Any):
        
        if key == "canvas_background":
            if self.properties["canvas_background"] == 1:
                print("making pixel map")
                size = 50
                pm = QPixmap(size, size)
                pm.fill(Qt.white)

                p = QPainter(pm)
                p.setPen(QColor(220, 220, 220))
                p.drawLine(0, 0, size, 0)
                p.drawLine(0, 0, 0, size)
                p.end()

                self.setBackgroundBrush(pm)
            else:
                self.setBackgroundBrush(QColor(Qt.white))
        pass
            

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
    
    def start_connection(self, source_node, pos):
        from PySide6.QtWidgets import QGraphicsLineItem
        line = QGraphicsLineItem(pos.x(), pos.y(), pos.x(), pos.y())
        line.setPen(QPen(Qt.black, 2, Qt.DashLine))
        self.scene().addItem(line)
        self._current_connection = {"source_node": source_node, "temp_line": line}



    # context menu API
    def _add_block_from_menu(self):
        if self._rc_scene_pos is None:
            return
        self.add_block(self._rc_scene_pos.x(), self._rc_scene_pos.y())

    def _add_corner_from_menu(self):
        if self._rc_scene_pos is None:
            return
        self.add_corner(self._rc_scene_pos.x(), self._rc_scene_pos.y())

    """
    The canvas has a scene rectangle, which can be smaller than the viewport rectangle. This ensures that the scene expands when you pan around.
    """
    def ensure_prehaps_expand_scene_rect(self):
        scene = self.scene()
        if not scene:
            return
        if not self.properties["scene_resizable"]:
            return
        
        EXPAND_MARGIN = 500
        EXPAND_AMOUNT = 1000
        scene_rect = scene.sceneRect()
        view_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        new_rect = QRectF(scene_rect)

        if view_rect.left() < scene_rect.left() + EXPAND_MARGIN:
            new_rect.setLeft(scene_rect.left() - EXPAND_AMOUNT)

        if view_rect.right() > scene_rect.right() - EXPAND_MARGIN:
            new_rect.setRight(scene_rect.right() + EXPAND_AMOUNT)

        if view_rect.top() < scene_rect.top() + EXPAND_MARGIN:
            new_rect.setTop(scene_rect.top() - EXPAND_AMOUNT)

        if view_rect.bottom() > scene_rect.bottom() - EXPAND_MARGIN:
            new_rect.setBottom(scene_rect.bottom() + EXPAND_AMOUNT)

        if new_rect != scene_rect:
            scene.setSceneRect(new_rect)

