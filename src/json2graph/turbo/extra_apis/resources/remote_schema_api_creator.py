from typing import Any

import ray
from ebf.interfaces.resource_creator import ResourceCreator
from json2graph.schema_api import SchemaAPI
from json2graph.schema_api_definition import SchemaApiDefinition
from ebf.jobs.needs_central_api import NeedsCentralApi


class RemoteSchemaApiCreator(ResourceCreator[SchemaAPI], NeedsCentralApi):
    async def create(
        self,
        definition: SchemaApiDefinition,
        meta: dict[str, Any] | None = None,
    ):
        actor_ref = ray.remote(SchemaAPI).remote(
            definition,
        )

        return actor_ref
