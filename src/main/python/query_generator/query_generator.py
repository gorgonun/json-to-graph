from main.python.node import Node
from main.python.query_generator.neo4j.neo4j_query_generator import Neo4jQueryGenerator


class QueryGenerator():
    def __init__(self, mode: str):
        self.__mode = mode
    
    def generate(self, nodes: list[Node]):
        if self.__mode == "neo4j":
            return Neo4jQueryGenerator().generate_query(nodes)
        else:
            raise RuntimeError(f"Invalid mode {self.__mode}")
