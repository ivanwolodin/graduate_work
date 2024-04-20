import orjson
from pydantic import BaseModel


class BaseContent(BaseModel):

    user_id: str
    content_type: str
    metrics: int

    class Config:
        json_loads = orjson.loads
