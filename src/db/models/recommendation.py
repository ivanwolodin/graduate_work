from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON

from ..base import  Base


class Recommendation(Base):
    __tablename__ = "recomendations"

    user_id = Column(Integer, primary_key=True)
    list_of_recommendations = Column(JSON, unique=True, index=True)

