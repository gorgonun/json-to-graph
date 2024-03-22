from dataclasses import dataclass
from ebf.event_based_boolean_scheduler.events.event import Event


@dataclass
class Neo4JNodeCreated(Event):
    id: int
    label: str
    processing_id: str
