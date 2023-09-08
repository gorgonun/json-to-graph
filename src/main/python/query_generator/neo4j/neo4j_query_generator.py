from main.python.node import Node
from main.python.query_generator.neo4j.node_query_generator import NodeQueryGenerator


class Neo4jQueryGenerator():
    def __init__(self, node_query_generator: NodeQueryGenerator | None = None) -> None:
        self.node_query_generator = node_query_generator or NodeQueryGenerator()

    def generate_query(self, nodes: list[Node]):
        return self.node_query_generator.generate_query(nodes)
