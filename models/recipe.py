#!/usr/bin/python3
""" Place Module for HBNB project """
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.rating import Rating
import models

Favourite = Table(
    'favourite',
    Base.metadata,
    Column('user_id', String(60), ForeignKey('users.id'),
           primary_key=True, nullable=False),
    Column('recipe_id', String(60), ForeignKey('recipes.id'),
           primary_key=True, nullable=False)
)


class Recipe(BaseModel, Base):
    """This class defines the table 'places' by various
    attributes(columns) for the database storage"""
    __tablename__ = 'recipes'
    title = Column(String(128), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    comments = []
    if os.getenv('HBNB_TYPE_STORAGE', 'db') == 'db':
        ratings = relationship("Rating", cascade='all, delete-orphan',
                               backref="recipe")
        favourites = relationship('User', secondary=Favourite,
                                  backref='saved_recipes', viewonly=False)
    else:
        @property
        def ratings(self):
            """Returns the reviews associated with Place"""
            ratings_in_place = []
            # getting a list of values from the all() dictionary and looping
            for value in models.storage.all(Rating).values():
                if value.place_id == self.id:
                    ratings_in_place.append(value)
            return ratings_in_place

        @property
        def comments(self):
            """Returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place"""
            from models.comment import Comment
            amenities_in_place = []
            # getting a list of values from the all() dictionary and looping
            # through to check if the id is in amenity_ids
            for value in models.storage.all(Comment).values():
                if value in self.comments:
                    amenities_in_place.append(value)
            return amenities_in_place

        @comments.setter
        def comments(self, comment_obj):
            """Setter that handles append method for adding an Amenity.id
            to the attribute amenity_ids"""
            from models.comment import Comment
            if type(comment_obj) == Comment:
                self.comments.append(comment_obj)
