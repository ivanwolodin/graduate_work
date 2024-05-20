import uuid
from typing import List, Optional, Union

from api.v1.models.api_base_model import Base
from api.v1.models.api_genre_models import Genre
from api.v1.models.api_person_models import PersonBase


class FilmBase(Base):
    title: str
    imdb_rating: Optional[float]


class Film(FilmBase):
    description: str = ''
    genre: Union[str, List[Genre]] = []
    actors: List[PersonBase] = []
    directors: List[PersonBase] = []
    writers: List[PersonBase] = []


class EsMovie(Base):
    uuid: uuid.UUID
    title: str
