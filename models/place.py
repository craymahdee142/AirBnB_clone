#!/usr/bin/python3
"""Defines place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place

    Attributes:
        city_id (str): The city id
        user_id (str): The user id
        name (str): The name of the place
        description (str): the description of the place
        num_of_romms (int): the number of rooms of the place
        num_of_bathrooms (int): the number of bathrooms of the place
        max_guest (int): maximum num of gust of the place
        price_by_night (int): Price per night
        latitude (float); The latitude of the place
        longitude (float): the longitude of the place
        amenity_ids (list): list of Amenity ids
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    num_of_rooms = 0
    num_of_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
