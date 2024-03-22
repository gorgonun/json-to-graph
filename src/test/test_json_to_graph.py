from json2graph.json_to_node import JsonToNode
from json2graph.node import Node
from json2graph.schema import Schema
from json2graph.schema_api import SchemaAPI
from json2graph.table import Table

def test_it_migrates_dict():
    test_dict = [
        {
            "_id": "1",
            "name": "John",
            "age": 20,
            "address": {
                "street": "Main Street",
                "number": 123,
                "city": "New York"
            },
            "phones": [
                {
                    "type": "mobile",
                    "number": "123456789"
                },
                {
                    "type": "home",
                    "number": "987654321"
                }
            ]
        }
    ]

    address_node = Node(
        id=2,
        table=Table(
            id=2,
            name="address",
            schema=Schema(
                id=2,
                column_information={
                    "street": False,
                    "number": False,
                    "city": False
                }
            ),
            path=[],
            relations=[]
        ),
        relations=[],
        values={
            "street": "Main Street",
            "number": 123,
            "city": "New York"
        }
    )

    phone1_node = Node(
        id=3,
        table=Table(
            id=3,
            name="phones",
            schema=Schema(
                id=3,
                column_information={
                    "type": False,
                    "number": False,
                }
            ),
            path=[],
            relations=[]
        ),
        relations=[],
        values={
            "type": "mobile",
            "number": "123456789"
        }
    )

    phone2_node = Node(
        id=4,
        table=Table(
            id=3,
            name="phones",
            schema=Schema(
                id=3,
                column_information={
                    "type": False,
                    "number": False,
                }
            ),
            path=[],
            relations=[],
        ),
        relations=[],
                    values={
                "type": "mobile",
                "number": "123456789"
            }
    )

    expected = Node(
        id=1,
        table=Table(
            id=1,
            name="test",
            schema=Schema(
                id=1,
                column_information={
                    "_id": False,
                    "name": False,
                    "age": False,
                    "address": False,
                    "phones": False
                }
            ),
            relations=[],
            path=[]
        ),
        relations=[
            address_node,
            phone1_node,
            phone2_node
        ],
        values={
            "_id": "1",
            "name": "John",
            "age": 20,
        }
    )

    schema = SchemaAPI(0.5)
    json_to_graph = JsonToNode("test", schema)
    
    result = json_to_graph.migrate_data(test_dict)
    print(result)

    assert result == [expected]


# def test_it_migrates_dict_2():
    # test_dict = [
    #     {
    #         "_id": "1",
    #         "name": "John",
    #         "age": 20,
    #         "address": {
    #             "street": "Main Street",
    #             "number": 123,
    #             "city": "New York"
    #         },
    #         "phones": [
    #             {
    #                 "type": "mobile",
    #                 "number": "123456789"
    #             },
    #             {
    #                 "type": "home",
    #                 "number": "987654321"
    #             }
    #         ],
    #         "cars": [
    #             {
    #                 "brand": "Ford",
    #                 "model": "Fiesta",
    #                 "stores": [
    #                     {
    #                         "name": "Store 1",
    #                         "address": {
    #                             "street": "Main Street",
    #                             "number": 123,
    #                             "city": "New York"
    #                         }
    #                     },
    #                 ]
    #             },
    #             {
    #                 "brand": "Ford 2",
    #                 "model": "Fiesta 2",
    #                 "stores": [
    #                     {
    #                         "name": "Store 2",
    #                         "address": {
    #                             "street": "Main Street",
    #                             "number": 123,
    #                             "city": "New York"
    #                         }
    #                     },
    #                     {
    #                         "name": "Store 3",
    #                         "address": {
    #                             "street": "Main Street 2",
    #                             "number": 1234,
    #                             "city": "New York City"
    #                         }
    #                     },
    #                 ]
    #             }
    #         ]
    #     }
    # ]

    # address_node = Node(
    #     id=2,
    #     table=Table(
    #         id=2,
    #         name="address",
    #         schema=Schema(
    #             id=2,
    #             column_information={
    #                 "street": False,
    #                 "number": False,
    #                 "city": False
    #             }
    #         ),
    #         path=[],
    #         relations=[]
    #     ),
    #     relations=[]
    # )

    # phone1_node = Node(
    #     id=3,
    #     table=Table(
    #         id=3,
    #         name="phones",
    #         schema=Schema(
    #             id=3,
    #             column_information={
    #                 "type": False,
    #                 "number": False,
    #             }
    #         ),
    #         path=[],
    #         relations=[]
    #     ),
    #     relations=[]
    # )

    # phone2_node = Node(
    #     id=4,
    #     table=Table(
    #         id=3,
    #         name="phones",
    #         schema=Schema(
    #             id=3,
    #             column_information={
    #                 "type": False,
    #                 "number": False,
    #             }
    #         ),
    #         path=[],
    #         relations=[]
    #     ),
    #     relations=[]
    # )

    # expected = Node(
    #     id=1,
    #     table=Table(
    #         id=1,
    #         name="test",
    #         schema=Schema(
    #             id=1,
    #             column_information={
    #                 "_id": False,
    #                 "name": False,
    #                 "age": False,
    #                 "address": False,
    #                 "phones": False
    #             }
    #         ),
    #         relations=[],
    #         path=[]
    #     ),
    #     relations=[
    #         address_node,
    #         phone1_node,
    #         phone2_node
    #     ]
    # )

    # schema = SchemaAPI(0.5)
    # json_to_graph = JsonToGraph("test", schema)
    
    # result = json_to_graph.migrate_data(test_dict)

    # assert result == [expected]
