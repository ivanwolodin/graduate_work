from uuid import UUID
from functools import lru_cache
from sqlalchemy.orm import Session
from ..db.models.recommendation import Recommendation
from ..db.session import SessionLocal


class RecommendationService:
    def __init__(self, session: Session):
        self.db = session

    async def get_recommendations(self, user_id: UUID) -> Recommendation:
        return self.db.query(Recommendation).get(user_id)


@lru_cache()
async def get_rec_service() -> RecommendationService:
    return RecommendationService(SessionLocal)
