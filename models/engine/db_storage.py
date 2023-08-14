#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.comment import Comment
from models.base_model import Base
from models.recipe import Recipe
from models.rating import Rating
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Comment": Comment, "Recipe": Recipe,
           "Rating": Rating, "User": User}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER', 'pycharm')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD', 'pycharm')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', 'localhost')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB', 'foorec')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, cls_id):
        """ Retrieves an object from the database. """
        if cls in classes.keys() or cls in classes.values():
            if isinstance(cls, str):
                cls = eval(cls)
            return self.__session.query(cls).filter_by(id=cls_id).first()
        return None

    def get_user(self, username):
        """ Retrieves an object from the database. """
        return self.__session.query(User).filter_by(username=username).first()

    def count(self, cls=None):
        """ Counts the number of objects in storage. """
        if cls is None or cls in classes.keys() or cls in classes.values():
            return len(self.all(cls))
