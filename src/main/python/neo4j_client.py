from neo4j import Driver, GraphDatabase

from main.python.node import Node
from main.python.query_generator.neo4j.neo4j_query_generator import Neo4jQueryGenerator


class Neo4jClient():
    def __init__(self, driver: Driver | None = None, url: str | None = None, neo4j_user: str | None = None, neo4j_password: str | None = None) -> None:
        self.driver = driver
        self.query_generator = Neo4jQueryGenerator()
        self.__url = url
        self.__neo4j_user = neo4j_user
        self.__neo4j_password = neo4j_password

    def write_nodes(self, nodes: list[Node]):
        with self.driver.session() as session:
            for (query, nodes_values) in self.query_generator.generate_create_query(nodes):
                print(query, nodes_values)
                session.run(query, nodes=nodes_values)

            for query in self.query_generator.generate_query_for_relationship(nodes):
                session.run(query)

    def __enter__(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(self.__url, auth=(self.__neo4j_user, self.__neo4j_password))
            self.driver.verify_connectivity()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.close()
        return
    
    @classmethod
    def from_url(cls, url: str, neo4j_user: str, neo4j_password: str):
        return cls(url=url, neo4j_user=neo4j_user, neo4j_password=neo4j_password)
