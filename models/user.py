#!/usr/bin/python3
"""Defines the User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Repreent a user

    Attributes:
        email (str): Email of user
        password (str): password of user
        first_name (str): first name of the user
        last_name (str): last name of the user
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
