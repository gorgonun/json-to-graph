from neo4j import Driver, GraphDatabase

from main.python.node import Node
from main.python.query_generator.query_generator import QueryGenerator


class Neo4jClient():
    def __init__(self, driver: Driver | None = None, url: str | None = None, neo4j_user: str | None = None, neo4j_password: str | None = None, query_generator: QueryGenerator = None) -> None:
        self.driver = driver
        self.query_generator = query_generator or QueryGenerator("neo4j")
        self.__url = url
        self.__neo4j_user = neo4j_user
        self.__neo4j_password = neo4j_password

    def write_nodes(self, nodes: list[Node]):
        for query in self.query_generator.generate(nodes):
            print(query)
        # with self.driver.session() as session:
        #     for (query, nodes) in self.query_generator.generate(nodes):
        #         session.run(query, nodes=nodes)

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
