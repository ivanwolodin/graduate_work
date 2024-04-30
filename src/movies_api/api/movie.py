"""Endpoints for getting movie information."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from ..schemas.movie import MovieResponse
from ..services.movie import MovieService, get_movie_service

movie_router = APIRouter()


@movie_router.get(
    "/movie/{movie_id}", response_model=MovieResponse
)
async def recommendation(
        movie_id: UUID,
        rec_service: MovieService = Depends(get_movie_service)
):
    try:
        res = await rec_service.get_movie(movie_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    return MovieResponse(
        title=res.title,
        description=res.description,
        imdb_rating=res.imdb_rating
    )
