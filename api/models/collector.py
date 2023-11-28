from bunnet import Document
from pydantic import Field
from uuid import UUID, uuid4


class Collector(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str
    owner: None = None
