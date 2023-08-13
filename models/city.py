#!/usr/bin/python3
"""Defines a city class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city

    Attributes:
        state_id (str): the state id
        name (str): the name of the city
    """

    state_id = ""
    name = ""
