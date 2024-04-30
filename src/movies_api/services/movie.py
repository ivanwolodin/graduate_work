from uuid import UUID
from functools import lru_cache

from sqlalchemy import select
from ..db.models.movies import Movie
from ..db.session import session_scope


class MovieService:
    async def get_movie(self, id: UUID) -> Movie:
        with session_scope() as session:
            res = session.scalars(
                select(
                    Movie
                ).where(Movie.movie_id == id)).one()
            session.expunge(res)
            return res


@lru_cache()
def get_movie_service() -> MovieService:
    return MovieService()
