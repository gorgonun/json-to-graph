from typing import Any
from main.python.node import Node


class NodeQueryGenerator():
    def merge_nodes_by_label(self, nodes: list[Node]):
        labels = {}
        for node in nodes:
            labels.setdefault(node.table.name, []).append(node)
        
        return labels

    def generate_create_query(self, nodes: list[Node]):
        nodes_by_label = self.merge_nodes_by_label(nodes)

        for label, nodes in nodes_by_label.items():
            yield self.generate_query_for_label(label, nodes)
    
    def generate_query_for_label(self, label: str, nodes: list[Node]):
        row_query = self.generate_query_for_row(nodes[0])

        return (
        f"""
            WITH $nodes AS nodes
            UNWIND nodes AS node
            MERGE (n:{self.scape_label(label)})
            ON CREATE\n {row_query}
            """,
            [node.common_values for node in nodes]
        )
    
    def generate_query_for_row(self, node: Node) -> str:
        result = []

        for column in node.table.schema.column_information.values():
            if not column.is_relationship:
                result.append(f"n.{self.scape_label(column.name)} = node.{column.name}")
        
        return "SET " + ",\n".join([*result])

    def generate_query_for_relationship(self, nodes: list[Node]) -> str:
        for node in nodes:
            for relation in node.relations:
                yield f"MERGE (n: {node.table.name} {{id: {node.id}}})-[:{self.scape_label(relation.table.name)}]->({relation.table.name} {{id: {relation.id}}})"

    def scape_label(self, label: str) -> str:
        # convert \u0060 to literal backtick and then escape backticks
        return label.replace("\\u0060", "`").replace("`", "``")
