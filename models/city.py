#!/usr/bin/python3
""" Define city module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ Define a City class

        Attributes:
            state_id (str): The state id.
            name (str): The name of the city.
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'))
    places = relationship("Place", backref="cities", cascade="all, delete")
