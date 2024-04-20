#!/usr/bin/python3
""" Defines a FileStorage """
import json
import os.path as p
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class FileStorage:
    """ Define a FileStorage class """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls is None:
            return type(self).__objects
        return {k: v for k, v in type(self).__objects.items()
                if type(v) is cls}

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """

        key = "{}.{}".format(type(obj).__name__, obj.id)
        type(self).__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """

        obj = {}
        for k, v in type(self).__objects.items():
            obj[k] = v.to_dict()

        with open(type(self).__file_path, 'w', encoding="utf-8") as f:
            json.dump(obj, f)

    def reload(self):
        """
            Deserializes the JSON file to __objects
            (only if the JSON file ( __file_path ) exists
        """

        classes = {"BaseModel": BaseModel, "User": User, 'Amenity': Amenity,
                   'City': City, 'State': State, 'Place': Place,
                   'Review': Review}
        obj_dict = {}
        if p.exists(type(self).__file_path):
            with open(type(self).__file_path, 'r', encoding="utf-8") as f:
                obj_dict = json.load(f)

        for k, v in obj_dict.items():
            cls = classes.get(v["__class__"])
            obj_instance = cls(**v)
            type(self).__objects[k] = obj_instance

    def delete(self, obj=None):
        """ Delete obj from __objects if it's inside """

        if obj:
            if obj in type(self).__objects.values():
                k = "{}.{}".format(type(obj).__name__, obj.id)
                del type(self).__objects[k]
                self.save()

    def close(self):
        """ Deserializing the JSON file to objects """

        self.reload()
