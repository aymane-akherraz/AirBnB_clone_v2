#!/usr/bin/python3
""" Defines a DBStorage """
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class DBStorage:
    """ Define a DBStorage class """

    __engine = None
    __session = None
    classes = [User, Amenity, City, State, Place, Review]

    def __init__(self):
        """ create the engine """

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session
            all objects depending of the class name
        """
        my_dict = {}
        if cls is None:
            for c in DBStorage.classes:
                res = self.__session.query(c).all()
                for obj in res:
                    k = "{}.{}".format(type(obj).__name__, obj.id)
                    if hasattr(obj, "_sa_instance_state"):
                        del obj._sa_instance_state
                    my_dict[k] = obj
        else:
            for c in DBStorage.classes:
                if c == cls:
                    res = self.__session.query(cls).all()
                    for obj in res:
                        k = "{}.{}".format(type(obj).__name__, obj.id)
                        if hasattr(obj, "_sa_instance_state"):
                            del obj._sa_instance_state
                        my_dict[k] = obj
                    break
        return my_dict

    def new(self, obj):
        """ Add the object to the current database session """

        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and
            the current database session
        """

        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Close scoped session
        """
        self.__session.remove()
