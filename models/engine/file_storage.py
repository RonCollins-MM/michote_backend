#!/usr/bin/python3

"""FileStorage engine module.

This module handles file storage for all the modules.
"""

import os
import json
import models
from models.base_model import BaseModel
from models.admin import Admin
from models.booked_trip import BookedTrip
from models.partner import Partner
from models.customer import Customer
from models.route import Route

class FileStorage():
    """FileStorage implementation class."""

    __file_path = 'models.json'
    __objects = {}

    __classes = {'Customer': Customer, 'Partner': Partner,
                 'BookedTrip': BookedTrip, 'Admin': Admin,
                 'Route': Route
    }

    def __init__(self):
        """Constructor"""
        pass

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls == None:
            return self.__objects
        filtered_dict = {}
        for key, value in self.__objects.items():
            if cls == value.__class__ or cls == value.__class__.__name__:
                filtered_dict[key] = value
        return filtered_dict

    def new(self, obj):
        """Adds a new object to __objects with the key <class_name>.<id>"""

        new_key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects.update({new_key : obj})

    def save(self):
        """Serializes __objects to the JSON file in __file_path"""

        lcl_copy = self.__objects
        objects_as_dict = {key: lcl_copy[key].to_dict() for key in
                           lcl_copy.keys()}

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

    def delete(self, obj=None):
        """Delete object from __objects if it exists"""
        if obj == None:
            return
        key = f'{obj.__class__.__name__}.{obj.id}'
        if key in self.__objects:
            del self.__objects[key]
            print("!! Object DELETED !!")

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieves an object from storage"""
        if cls not in FileStorage.__classes.values():
            return None

        objs_dict = models.storage.all(cls)
        for obj in objs_dict.values():
            if (obj.id == id):
                return obj

        return None

    def count(self, cls=None):
        """Counts the number of objects of a given class in storage"""
        return len(self.all(cls))
