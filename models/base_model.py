#!/usr/bin/python3
"""Defines the BaseModel class"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """representation of airbnb project"""

    def __init__(self, *args, **kwargs):
        """Initialize a new Base model

        Args:
            *args (any): unused
            **kwargs (dict): key/value pairs of attributes
        """
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, date_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Update 'updated_at' instance with current datetime"""
        self.updated_at = date.today()
        models.storage.save()

    def to_dict(self):
        """Dictionary representation of the model

        Include the key/value pair __class__ representing the class name
        of the object.
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict

    def __str__(self):
        """retern the str representation of of the BaseModel instance"""
        cl_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cl_name, self.id, self.__dict__)
