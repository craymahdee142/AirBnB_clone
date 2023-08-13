#!/usr/bin/python3
"""Defines state class"""
from models.base_model import BaseModel


class State(BaseModel):
    """represent s state

    Attributes:
        name (str): name of the state
    """

    name = ""
