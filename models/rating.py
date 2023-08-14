#!/usr/bin/python
""" holds class Rating"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Rating(BaseModel, Base):
    """Representation of Rating"""
    if models.storage_t == 'db':
        __tablename__ = 'ratings'
        recipe_id = Column(String(60), ForeignKey('recipes.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        rating = Column(Integer, nullable=False)
    else:
        recipe_id = ""
        user_id = ""
        rating = ""

    def __init__(self, *args, **kwargs):
        """initializes Rating"""
        super().__init__(*args, **kwargs)
