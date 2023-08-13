#!/usr/bin/python3
"""File storage.py module"""

import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """Represent an abstracted storage engine

    Attributes:
        __file_path (str): name of file to save object to
        __objects (dict): dictionary of instantiated objec
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """public instance method that returns dict __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """public instance method that sets in __objects
        the obj with key <obj class name>.id
        """
        obj_cls_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_cls_name, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)

        new_dict {dict} keys and values to build JSON.
        """
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict().copy()
        with open(FileStorage.__file_path, "w") as file:
            json.dump(new_dict, file)

    def reload(self):
        """public instance method that deserializes a JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, "r") as file:
                new_dict = json.load(file)
                for key, value in new_dict.items():
                    class_name = value.get("__class__")
                    obj = eval(class_name + "(**value)")
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
