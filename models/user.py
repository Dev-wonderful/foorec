#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        username = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        ratings = relationship("Rating", backref="user", cascade="delete")
        comments = relationship("Comment", backref="user", cascade="delete")
        favourites = relationship("Favourite", backref="user", cascade="delete")
    else:
        username = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        hash = md5()
        if kwargs:
            hash.update(kwargs["password"].encode('utf-8'))
            kwargs["password"] = hash.hexdigest()
        super().__init__(*args, **kwargs)
