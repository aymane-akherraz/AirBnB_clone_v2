#!/usr/bin/python3
""" Define amenity module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Define a Amenity class
        Attributes:
            name (str): The name of the amenity.
    """

    __tablename__ = "amenities"
    __table_args__ = {'mysql_collate': 'latin1_swedish_ci'}
    name = Column(String(128), nullable=False)
