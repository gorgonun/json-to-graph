import asyncio
import os
from typing import Any
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv
from python.async_relationship_reference import AsyncRelationshipReference
from python.events.neo4j_node_created import Neo4JNodeCreated
from python.json_to_node import JsonToNode
from python.neo4j_client import Neo4jClient
from python.neo4j_relationship_data import Neo4JRelationshipData
from python.node import Node, PartialNode
from ebf.decorators.job import job
from ebf import turbo
from python.schema_api import SchemaAPI
import logging
from ebf.event_based_boolean_scheduler.event_based_boolean_scheduler import EventBasedBooleanScheduler

from python.subnode_processing_request import SubNodeProcessingRequest
from ebf.jobs.dynamic_job.dynamic_job_helper_api import DynamicJobHelperApi
from ebf.interfaces.queue_api import QueueApi
from ebf.event_based_boolean_scheduler.decorators.event_job import event_job
from ebf.event_based_boolean_scheduler.operators.expression_helpers import event_happened
from ebf.event_based_boolean_scheduler.decorators.handler import when
from ebf.event_based_boolean_scheduler.commands.register_handler_command import RegisterHandlerCommand

logging.basicConfig(level=logging.INFO)

neo4j_log = logging.getLogger("neo4j")
neo4j_log.setLevel(logging.DEBUG)

event_based_boolean_scheduler = EventBasedBooleanScheduler()

load_dotenv()

def handler(origin_id, origin_label, destination_processing_id, relationship_name):
    def trigger(relationship_name: str):
        def wrapper(content: Neo4JNodeCreated):
            # content is the last created node, so we can use the created id to create the relationship
            destination_event = content
            return Neo4JRelationshipData(
                origin_id=origin_id,
                origin_label=origin_label,
                destination_id=destination_event.id,
                destination_label=content.label,
                relationship_name=relationship_name
            )
        
        return wrapper

    relationship_handler = when(
        predicate=(
            event_happened(Neo4JNodeCreated.ref(id=origin_id)) &
            event_happened(Neo4JNodeCreated.ref(processing_id=destination_processing_id))
        ),
        outputs=["neo4j_create_relationship_queue"]
    )(trigger(relationship_name))

    return relationship_handler


async def on_subnode(client: JsonToNode, api: DynamicJobHelperApi, feedback_queue: QueueApi):
    async def with_client_and_queue(node: PartialNode, src_column: str, level: int, sub_node: dict[str, Any]):
        reference = AsyncRelationshipReference(uuid.uuid4().hex)

        relationship_handler = handler(node.id, node.table.name, str(reference), src_column)
        await api.central_api.execute(RegisterHandlerCommand(relationship_handler))

        node.relations.append(reference)
        await feedback_queue.put({**sub_node, "processing_id": reference})
        return reference
    return with_client_and_queue


@job(single_run=True, output_queues_references=["mongodb_producer_output"], environ={"mongodb_url": os.environ["MONGODB_URL"], "mongodb_database": os.environ["MONGODB_DATABASE"], "mongodb_collection": os.environ["MONGODB_COLLECTION"]})
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

@job(input_queue_reference="mongodb_producer_output", output_queues_references=["json_to_node_output"], client=JsonToNode(os.environ["MONGODB_COLLECTION"], SchemaAPI(0.5)))
async def json_to_node(content: dict[str, Any], client: JsonToNode, api: DynamicJobHelperApi):
    nodes = await client.migrate_data(content, on_subnode=await on_subnode(client, api, api.queues["mongodb_producer_output"]))
    return nodes

@event_job(event_based_boolean_scheduler)(input_queue_reference="json_to_node_output", internal_state={"write_count": 0}, clients_with_context={"neo4j": Neo4jClient.from_url(os.environ["NEO4J_URL"], os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])}, meta={"dispatches": [Neo4JNodeCreated]})
async def node_to_neo4j(content: Node, internal_state, neo4j: Neo4jClient):
    neo4j.write_node(content)
    internal_state["write_count"] = internal_state["write_count"] + 1
    result = Neo4JNodeCreated(id=content.id, label=content.table.name, processing_id=content.processing_id)
    print("wrote", internal_state["write_count"])
    return result


@job(input_queue_reference="neo4j_create_relationship_queue", internal_state={"write_count": 0}, clients_with_context={"neo4j": Neo4jClient.from_url(os.environ["NEO4J_URL"], os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])})
async def neo4j_create_relationship(content: Neo4JRelationshipData, internal_state, neo4j: Neo4jClient, api: DynamicJobHelperApi):
    neo4j.create_relationship(content)
    internal_state["write_count"] = internal_state["write_count"] + 1
    print("wrote relationships", internal_state["write_count"], "from", content.origin_id, "to", content.destination_id)


async def main(threshold: float = 0.5):
    scheduler, central_api = await turbo.create(event_based_boolean_scheduler)

    await scheduler.start()


if __name__ == '__main__':
    asyncio.run(main())
