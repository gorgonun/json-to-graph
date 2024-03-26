from typing import Hashable
from ebf.extra_api.command.definition_command import DefinitionCommand
from json2graph.turbo.extra_apis.resources.json_to_graph_enum import JsonToGraphEnum
from json2graph.turbo.extra_apis.resources.remote_schema_api_api import RemoteSchemaApiApi


class SchemaApiControllerDefinition(DefinitionCommand[Hashable, RemoteSchemaApiApi]):
    api_identifier = JsonToGraphEnum.API_ID.value
    api_path = "remote_schema_api_controller_controllers/controller"
