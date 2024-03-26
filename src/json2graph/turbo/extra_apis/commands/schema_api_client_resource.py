from ebf.extra_api.command.crud_client_resource_command import CrudClientResourceCommand

from json2graph.schema_api import SchemaAPI
from json2graph.schema_api_definition import SchemaApiDefinition
from json2graph.turbo.extra_apis.resources.interfaces.schema_api_api import (
    SchemaApiApi,
)
from json2graph.turbo.extra_apis.resources.json_to_graph_enum import JsonToGraphEnum


class SchemaApiClientResource(
    CrudClientResourceCommand[SchemaApiDefinition, SchemaAPI, SchemaApiApi]
):
    api_identifier = JsonToGraphEnum.API_ID.value
    api_path = "schema_api/controllers/controller"
