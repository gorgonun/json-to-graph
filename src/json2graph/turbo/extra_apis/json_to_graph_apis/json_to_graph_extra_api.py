from ebf.extra_api.crud_client_resource_api import CrudClientResourceApi
from ebf.extra_api.default_extra_api_with_sub_apis import DefaultExtraApiWithSubApis
from ebf.extra_api.definition_resource_api import DefinitionResourceApi

from json2graph.schema_api_definition import SchemaApiDefinition
from json2graph.turbo.extra_apis.commands.schema_api_client_resource import SchemaApiClientResource
from json2graph.turbo.extra_apis.commands.schema_api_controller_definition import (
    SchemaApiControllerDefinition,
)
from json2graph.turbo.extra_apis.commands.schema_api_creator_definition import SchemaApiCreatorDefinition
from json2graph.turbo.extra_apis.resources.json_to_graph_enum import JsonToGraphEnum


class JsonToGraphExtraApi(DefaultExtraApiWithSubApis):
    def __init__(self) -> None:
        self.__apis = [
            DefinitionResourceApi(SchemaApiControllerDefinition),
            DefinitionResourceApi(SchemaApiDefinition),
            CrudClientResourceApi(
                SchemaApiClientResource,
                creators_keys=SchemaApiCreatorDefinition.get_api_reference().complete_id_path,
                apis_keys=SchemaApiControllerDefinition.get_api_reference().complete_id_path,
            ),
        ]
        super().__init__(
            [
                *[
                    command
                    for api in self.__apis
                    for command in api.get_command_structure()
                ],
            ],
            JsonToGraphEnum.API_ID.value,
        )

    @property
    def apis(self):
        return self.__apis
