"""Endpoints for getting recommendation information."""
from uuid import UUID

from fastapi import APIRouter, Depends
from ..schemas.recomendation import RecommendationResponse
from ..services.recommendation import RecommendationService, get_rec_service

recommendation_router = APIRouter()


@recommendation_router.get(
    "/recommendation/{user_id}", response_model=RecommendationResponse
)
async def recommendation(
        user_id: UUID,
        rec_service: RecommendationService = Depends(get_rec_service)
):
    res = rec_service.get_recommendations(user_id)
    return RecommendationResponse(list_of_recommendations=res.list_of_recommendations)