#!/usr/bin/python3

"""FileStorage engine module.

This module handles file storage for all the modules.
"""

import os
import json
from models.base_model import BaseModel

class FileStorage():
    """FileStorage implementation class."""

    __file_path = 'michote_models.json'
    __objects = {}

    def __init__(self):
        """Constructor"""
        pass

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to __objects with the key <class_name>.<id>"""

        new_key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects.update({new_key : obj})

    def save(self):
        """Serializes __objects to the JSON file in __file_path"""

        objects_as_dict = {key: self.__objects[key].to_dict() for key in
                           self.__objects.keys()}

        with open(self.__file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(objects_as_dict))

    def reload(self):
        """Deserializes the JSON file to __objects"""

        dict_of_objects = {}
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as json_file:
                dict_of_objects = json.loads(json_file.read())

        for obj in dict_of_objects.values():
            obj_to_add = eval(obj['__class__'])(**obj)
            self.new(obj_to_add)


