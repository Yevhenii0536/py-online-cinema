from sqlalchemy import Column, Integer, String, Float
from models.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)

    __repr__ = lambda self: f"{self.title} - {self.genre} - {self.price}"
