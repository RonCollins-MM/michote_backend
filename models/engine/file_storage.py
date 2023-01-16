#!/usr/bin/python3

"""File storage engine for Michote"""

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
    """Handles file storage engine
    
    Attributes
    ----------
    __file_path : str
        Path to the file storage
    
    __objects : dict
        Will hold all the objects that are retreived from storage

    __classes : dict
         All valid classes in the Michote app. This private dict is used for
        validation to ensure only objects of valid classes are created.  
    """

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
        """Returns the dict that contains all the objects that have been loaded
        from storage.
        
        If class name is provided, only objects from that class are returned.
        Otherwise, all objects in storage are returned.

        Parameters
        ----------
        cls : str, optional
            The class name whose objects are to be returned.

        Returns
        -------
        dict
            All objects that have been fetched from storage
        """
        if cls == None:
            return self.__objects
        filtered_dict = {}
        for key, value in self.__objects.items():
            if cls == value.__class__ or cls == value.__class__.__name__:
                filtered_dict[key] = value
        return filtered_dict

    def new(self, obj):
        """Adds a new object to storage with the key <class_name>.<id>
        
        Parameters
        ----------
        obj : object
            Object to be added to storage
        """

        new_key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects.update({new_key : obj})

    def save(self):
        """Serializes objects in the dict variable to the JSON file
        into the file given in the file path"""

        lcl_copy = self.__objects
        objects_as_dict = {key: lcl_copy[key].to_dict() for key in
                           lcl_copy.keys()}

        with open(self.__file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(objects_as_dict))

    def reload(self):
        """Deserializes the objects from storage into the dict variable"""

        dict_of_objects = {}
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as json_file:
                dict_of_objects = json.loads(json_file.read())

        for obj in dict_of_objects.values():
            obj_to_add = eval(obj['__class__'])(**obj)
            self.new(obj_to_add)

    def delete(self, obj=None):
        """Delete object from __objects if it exists.

        If no object is passed, does nothing.
        
        Parameters
        ----------
        obj : object, optional
            Object to be deleted from storage
        """
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
        """Retrieves an object from storage based on its class and ID.

        If class name or ID are invalid, does nothing.
        
        Parameters
        ----------
        cls : str
            The class name whose object is to be received
        
        id : str
            The ID of the object to be retreived
        """
        if cls not in FileStorage.__classes.values():
            return None

        objs_dict = models.storage.all(cls)
        for obj in objs_dict.values():
            if (obj.id == id):
                return obj

        return None

    def count(self, cls=None):
        """Counts the number of objects of a given class in storage.

        If no class is provided, all objects in storage are retreived.
        
        Parameters
        ----------
        cls : str
            The class whose object is to be retreived.
        """
        return len(self.all(cls))
