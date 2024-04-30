from typing import Optional

from sqlalchemy import Column, Integer, JSON, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from ..base import Base

JSONVariant = JSON().with_variant(JSONB(), "postgresql")


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(UUID, primary_key=True)
    title = Column(String)
    description = Column(String)
    imdb_rating = Column(Float)
