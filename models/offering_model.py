from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Offering(Base):
    __tablename__ = 'offerings'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    location = Column(String(255))
    price = Column(Float)
    rating = Column(Float)
    num_reviews = Column(Integer)
    platform_id = Column(String(255), unique=True)
