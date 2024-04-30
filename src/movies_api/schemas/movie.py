from typing import Optional
from pydantic import BaseModel


class MovieResponse(BaseModel):
    """Response for movies endpoint"""
    title: str
    description: str
    imdb_rating: Optional[float] = None
