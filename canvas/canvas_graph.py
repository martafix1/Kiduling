# canvas_graph.py

from typing import Dict, Any, List, Optional


class GraphNode:
    """Base class for all canvas nodes (blocks, corners, ports)."""

    _id_counter = 0

    def __init__(self, x: float, y: float, layer: str = "default", properties=None):
        self.id = GraphNode._id_counter
        GraphNode._id_counter += 1

        self.x = x
        self.y = y
        self.layer = layer
        self.properties: Dict[str, Any] = properties or {}

        self.edges: List["GraphEdge"] = []

    def attach_edge(self, edge: "GraphEdge"):
        if edge not in self.edges:
            self.edges.append(edge)

    def detach_edge(self, edge: "GraphEdge"):
        if edge in self.edges:
            self.edges.remove(edge)


class BlockNode(GraphNode):
    """Logical block node."""

    def __init__(self, x, y, layer="default", width=120, height=60, properties=None):
        super().__init__(x, y, layer, properties)
        self.properties.setdefault("width", width)
        self.properties.setdefault("height", height)


class CornerNode(GraphNode):
    """Routing-only node (not used in simulation)."""
    pass


class GraphEdge:
    """Connection between two GraphNodes."""

    _id_counter = 0

    def __init__(self, a: GraphNode, b: GraphNode, layer="default", properties=None):
        self.id = GraphEdge._id_counter
        GraphEdge._id_counter += 1

        self.a = a
        self.b = b
        self.layer = layer
        self.properties: Dict[str, Any] = properties or {}

        a.attach_edge(self)
        b.attach_edge(self)


class CanvasGraph:
    """The document model."""

    def __init__(self):
        self.nodes: Dict[int, GraphNode] = {}
        self.edges: Dict[int, GraphEdge] = {}

    # ---- node management ----

    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node
        return node

    def remove_node(self, node: GraphNode):
        for edge in node.edges[:]:
            self.remove_edge(edge)
        self.nodes.pop(node.id, None)

    # ---- edge management ----

    def add_edge(self, edge: GraphEdge):
        self.edges[edge.id] = edge
        return edge

    def remove_edge(self, edge: GraphEdge):
        edge.a.detach_edge(edge)
        edge.b.detach_edge(edge)
        self.edges.pop(edge.id, None)
