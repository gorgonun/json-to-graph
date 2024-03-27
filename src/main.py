import asyncio
import os
from typing import Any
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv
from json2graph.async_relationship_reference import AsyncRelationshipReference
from json2graph.events.neo4j_node_created import Neo4JNodeCreated
from json2graph.id_manager import IdManager
from json2graph.id_manager_api import IdManagerApi
from json2graph.json_to_node import JsonToNode
from json2graph.neo4j_client import Neo4jClient
from json2graph.neo4j_relationship_data import Neo4JRelationshipData
from json2graph.node import Node, PartialNode
from ebf.decorators.job import job
from ebf import turbo
from json2graph.node_feedback import NodeFeedback
import logging
from ebf.event_based_boolean_scheduler.event_based_boolean_scheduler import (
    EventBasedBooleanScheduler,
)
from ebf.jobs.dynamic_job.dynamic_job_helper_api import DynamicJobHelperApi
from ebf.interfaces.queue_api import QueueApi
from ebf.event_based_boolean_scheduler.decorators.event_job import event_job
from ebf.event_based_boolean_scheduler.operators.expression_helpers import (
    event_happened,
)
from ebf.event_based_boolean_scheduler.decorators.handler import when
from ebf.event_based_boolean_scheduler.commands.register_handler_command import (
    RegisterHandlerCommand,
)
from ebf.event_based_boolean_scheduler.interfaces.handler_properties import (
    HandlerProperties,
)
from ebf.event_based_boolean_scheduler.domain.handler_after_execution_property_enum import (
    HandlerAfterExecutionPropertyEnum,
)
from ebf.decorators.actor import actor, ActorDefinition

from json2graph.schema_api import SchemaAPI
from json2graph.turbo.extra_apis.resources.json_to_graph_enum import JsonToGraphEnum
from json2graph.turbo.extra_apis.resources.remote_schema_api_api import (
    RemoteSchemaApiApi,
)
from ebf.interfaces.central_api import CentralApi


logging.basicConfig(level=logging.INFO)

neo4j_log = logging.getLogger("neo4j")
neo4j_log.setLevel(logging.DEBUG)

event_based_boolean_scheduler = EventBasedBooleanScheduler()

load_dotenv()


@actor(
    name="schema_api",
    api=RemoteSchemaApiApi,
    api_identifier=JsonToGraphEnum.API_ID.value,
)
async def create_schema_api(_central_api: CentralApi):
    return ActorDefinition(
        actor_class=SchemaAPI, kwargs={"max_difference_between_schemas": 0.5}
    )


@actor(name="id_manager", api=IdManagerApi, api_identifier=JsonToGraphEnum.API_ID.value)
async def create_id_manager(_central_api: CentralApi):
    return ActorDefinition(actor_class=IdManager)


def handler(origin_id, origin_label, destination_processing_id, relationship_name):
    def trigger(relationship_name: str):
        def wrapper(content: Neo4JNodeCreated):
            # content is the last created node, so we can use the created id to create the relationship
            destination_event = content
            return Neo4JRelationshipData(
                origin_id=origin_id,
                origin_label=origin_label,
                destination_id=destination_event.id,
                destination_label=destination_event.label,
                relationship_name=relationship_name,
            )

        return wrapper

    relationship_handler = when(
        predicate=(
            event_happened(Neo4JNodeCreated.ref(id=origin_id))
            & event_happened(
                Neo4JNodeCreated.ref(processing_id=destination_processing_id)
            )
        ),
        outputs=["neo4j_create_relationship_queue"],
        handler_properties=HandlerProperties(
            after_true=HandlerAfterExecutionPropertyEnum.DELETE
        ),
    )(trigger(relationship_name))

    return relationship_handler


async def on_subnode(
    client: JsonToNode, api: DynamicJobHelperApi, feedback_queue: QueueApi
):
    async def with_client_and_queue(
        node: PartialNode, src_column: str, level: int, sub_node: dict[str, Any]
    ):
        reference = AsyncRelationshipReference(uuid.uuid4().hex)

        relationship_handler = handler(
            node.id, node.table.name, str(reference), src_column
        )
        await api.central_api.execute(RegisterHandlerCommand(relationship_handler))

        node.relations.append(reference)
        await feedback_queue.put(
            NodeFeedback(
                data=sub_node,
                processing_id=reference,
                level=level + 1,
                parent_field=src_column,
            )
        )
        return reference

    return with_client_and_queue


@job(
    single_run=True,
    output_queues_references=["mongodb_producer_output"],
    environ={
        "mongodb_url": os.environ["MONGODB_URL"],
        "mongodb_database": os.environ["MONGODB_DATABASE"],
        "mongodb_collection": os.environ["MONGODB_COLLECTION"],
    },
)
def mongodb_producer(environ: dict):
    mongodb_url = environ["mongodb_url"]
    mongodb_database = environ["mongodb_database"]
    mongodb_collection = environ["mongodb_collection"]

    client = MongoClient(mongodb_url)
    db = client[mongodb_database]
    collection = db[mongodb_collection]

    result = collection.find()

    for data in result:
        yield data


# Exclusive queue for feedback to decreate the size of handlers
@job(
    extra_queues_references=["mongodb_producer_output", "json_to_node_feedback"],
    output_queues_references=["json_to_node_output"],
    environ={"mongodb_collection": os.environ["MONGODB_COLLECTION"]},
)
async def json_to_node(
    fself,
    content: dict[str, Any] | NodeFeedback,
    environ: dict[str, str],
    api: DynamicJobHelperApi,
    on_first_run
):
    @on_first_run()
    async def __on_first_run(
        fself,
        content: dict[str, Any] | NodeFeedback,
        environ: dict[str, str],
        api: DynamicJobHelperApi,
        on_first_run,
    ):
        schema_api = await api.central_api.execute(
            (await create_schema_api(api.central_api)).resource_manager.get(
                "default"
            )
        )

        if not schema_api:
            raise RuntimeError("Schema API not found")

        id_manager = await api.central_api.execute(
            (await create_id_manager(api.central_api)).resource_manager.get("default")
        )

        if not id_manager:
            raise RuntimeError("Id Manager not found")

        fself["client"] = JsonToNode(environ["mongodb_collection"], schema_api, id_manager)

    await __on_first_run

    client: JsonToNode = fself["client"]
    nodes = await client.migrate_data(
        content,
        on_subnode=await on_subnode(client, api, api.queues["json_to_node_feedback"]),
    )
    return nodes


@event_job(event_based_boolean_scheduler)(
    input_queue_reference="json_to_node_output",
    clients_with_context={
        "neo4j": Neo4jClient.from_url(
            os.environ["NEO4J_URL"],
            os.environ["NEO4J_USER"],
            os.environ["NEO4J_PASSWORD"],
        )
    },
    meta={"dispatches": [Neo4JNodeCreated]},
    replicas=3
)
async def node_to_neo4j(fself, content: Node, neo4j: Neo4jClient, on_first_run, api: DynamicJobHelperApi,):
    @on_first_run()
    async def __on_first_run(
        fself,
        content: Neo4JRelationshipData,
        neo4j: Neo4jClient,
        api: DynamicJobHelperApi,
        on_first_run,
    ):
        id_manager = await api.central_api.execute(
            (await create_id_manager(api.central_api)).resource_manager.get("default")
        )

        fself["id_manager"] = id_manager

    await __on_first_run

    neo4j.write_node(content)
    result = Neo4JNodeCreated(
        id=content.id, label=content.table.name, processing_id=content.processing_id
    )
    print("wrote", await fself["id_manager"].get_id_increment("node_to_neo4j", create=True))
    return result


@job(
    input_queue_reference="neo4j_create_relationship_queue",
    clients_with_context={
        "neo4j": Neo4jClient.from_url(
            os.environ["NEO4J_URL"],
            os.environ["NEO4J_USER"],
            os.environ["NEO4J_PASSWORD"],
        )
    },
    replicas=2,
)
async def neo4j_create_relationship(
    fself,
    content: Neo4JRelationshipData,
    neo4j: Neo4jClient,
    api: DynamicJobHelperApi,
    on_first_run,
):
    @on_first_run()
    async def __on_first_run(
        fself,
        content: Neo4JRelationshipData,
        neo4j: Neo4jClient,
        api: DynamicJobHelperApi,
        on_first_run,
    ):
        id_manager = await api.central_api.execute(
            (await create_id_manager(api.central_api)).resource_manager.get("default")
        )

        fself["id_manager"] = id_manager

    await __on_first_run

    neo4j.create_relationship(content)
    print(
        "wrote relationships",
        await fself["id_manager"].get_id_increment("neo4j_create_relationship", create=True),
        "from",
        content.origin_id,
        "to",
        content.destination_id,
    )


async def main(threshold: float = 0.5):
    scheduler, central_api = await turbo.create(event_based_boolean_scheduler)
    await scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())
