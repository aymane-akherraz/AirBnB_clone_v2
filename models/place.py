#!/usr/bin/python3
""" Define place module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from os import getenv
from sqlalchemy.orm import relationship
import models
from models.review import Review
from models.amenity import Amenity


class Place(BaseModel, Base):
    """ Define a Place class

        Attributes:
            city_id (str): The City id.
            user_id (str): The User id.
            name (str): The name of the place.
            description (str): The description of the place.
            number_rooms (int): The number of rooms of the place.
            number_bathrooms (int): The number of bathrooms of the place.
            max_guest (int): The maximum number of guests of the place.
            price_by_night (int): The price by night of the place.
            latitude (float): The latitude of the place.
            longitude (float): The longitude of the place.
            amenity_ids (list): A list of Amenity ids.
    """

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True),
                          mysql_collate='latin1_swedish_ci')

    __tablename__ = "places"
    __table_args__ = {'mysql_collate': 'latin1_swedish_ci'}
    city_id = Column(String(60), ForeignKey('cities.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", backref="place_amenities",
                                 secondary="place_amenity",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ Returns the list of Review instances with
                place_id equals to the current Place.id
            """
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """ Returns the list of Amenity instances """

            return [amenity for amenity in models.storage.all(Amenity).values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, new_Amenity):
            """ Handles append method for adding an Amenity.id
                to the attribute amenity_ids
            """
            if type(new_Amenity) is Amenity:
                self.amenity_ids.append(new_Amenity.id)
