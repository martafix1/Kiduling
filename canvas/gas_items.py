

from base_items import BlockItem, CornerItem, ConnectionItem
from PySide6.QtGui import QPen, QColor



class GasBlock(BlockItem):
    pass  # add gas-specific properties

class GasCorner(CornerItem):
    pass

class GasPipe(ConnectionItem):
    def __init__(self, start_node, end_node):
        super().__init__(start_node, end_node)
        # Override pen for gas style
        self.pen = QPen(QColor("gold"), 4)  # thick yellow line
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.setPen(self.pen)