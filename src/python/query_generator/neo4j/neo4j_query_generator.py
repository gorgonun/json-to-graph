from python.neo4j_relationship_data import Neo4JRelationshipData
from python.node import Node
from python.query_generator.neo4j.node_query_generator import NodeQueryGenerator


class Neo4jQueryGenerator():
    def __init__(self, node_query_generator: NodeQueryGenerator | None = None) -> None:
        self.node_query_generator = node_query_generator or NodeQueryGenerator()

    def generate_create_query(self, nodes: list[Node]):
        yield from self.node_query_generator.generate_create_query(nodes)

    # def generate_query_for_relationship(self, nodes: list[Node]):
    #     yield from self.node_query_generator.generate_query_for_relationship(nodes)

    def generate_query_for_relationship(self, relationship_data: Neo4JRelationshipData):
        return self.node_query_generator.generate_query_for_relationship(relationship_data)
