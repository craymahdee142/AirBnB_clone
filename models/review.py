#!/usr/bin/python3
"""Defines review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review

    Attributes:
        place_id (str): the place id
        user_id (str): the user id
        text (str): text of the review
    """

    place_id = ""
    user_id = ""
    text = ""
