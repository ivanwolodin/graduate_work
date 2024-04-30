"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .version import version_router
from .movie import movie_router

api_router = APIRouter()
api_router.include_router(version_router, tags=["version"])
api_router.include_router(movie_router, tags=["version"])
