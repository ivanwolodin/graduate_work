from pydantic import BaseModel


class PaginatedParams(BaseModel):
    page_number: int = 1
    page_size: int = 50
