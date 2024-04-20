#!/usr/bin/python3
""" Define review module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Define a Review class

        Attributes:
            place_id (str): The Place id.
            user_id (str): The User id.
            text (str): The text of the review.
    """
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate': 'latin1_swedish_ci'}
    place_id = Column(String(60), ForeignKey('places.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    text = Column(String(1024), nullable=False)
