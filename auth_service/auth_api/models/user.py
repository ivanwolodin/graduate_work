from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.role import Role


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=True)
    second_name = Column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
