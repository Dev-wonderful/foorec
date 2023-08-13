#!/usr/bin/python
""" holds class Comment"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Comment(BaseModel, Base):
    """Representation of comments """
    if models.storage_t == 'db':
        __tablename__ = 'comments'
        text = Column(String(1024), nullable=False)
    else:
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
