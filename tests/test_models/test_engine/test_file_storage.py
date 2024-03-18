#!/usr/bin/python3
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
import json
import models
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class TestFilestorage(unittest.TestCase):
    """Test cases for the FileStorage class"""

    classes = [BaseModel, User, Amenity, City, State, Place, Review]

    def setUp(self):
        """ set up a clean state for running each test
            method within a test case
        """
        pass

    def tearDown(self):
        """clean up after each test method has executed"""

        FileStorage._FileStorage__objects = {}
        path = FileStorage._FileStorage__file_path
        if os.path.exists(path):
            os.remove(path)

    def test_initialization(self):
        """Test of initialization of Filestorage"""

        with self.assertRaises(TypeError):
            FileStorage(None)
        self.assertEqual(type(FileStorage()), FileStorage)
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)
        self.assertEqual(type(models.storage), FileStorage)

    def test_all(self):
        """ Test for the all method """

        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """ Test for the all method with one None """
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def create(self, obj):
        """Adds new objects to __objects dict of FileStorage"""

        models.storage.new(obj)

    def test_new(self):
        """Test for the new method"""

        for c in self.classes:
            obj = c()
            self.create(obj)
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.assertIn(key, FileStorage._FileStorage__objects.keys())
            self.assertIn(obj, FileStorage._FileStorage__objects.values())

    def test_new_with_args(self):
        """Test for the new method more than one arg"""

        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        """Test for the new method with None"""

        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        """Test for the save method"""

        my_list = []
        for c in self.classes:
            obj = c()
            my_list.append(json.dumps(obj.to_dict()))
            self.create(obj)
        models.storage.save()
        txt = ""
        with open("file.json", "r") as f:
            txt = f.read()

        for obj in my_list:
            self.assertIn(obj, txt)

    def test_save_with_arg(self):
        """Test for the save method with an arg"""

        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        """Test for the reload method"""

        my_list = []
        for c in self.classes:
            obj = c()
            my_list.append("{}.{}".format(type(obj).__name__, obj.id))
            self.create(obj)
        models.storage.save()
        models.storage.reload()

        for k in my_list:
            self.assertIn(k, FileStorage._FileStorage__objects.keys())

        def test_reload_with_arg(self):
            with self.assertRaises(TypeError):
                models.storage.reload(None)

        def test_reload_no_file(self):
        self.assertRaises(FileNotFoundError, models.storage.reload())

        def test_reload_with_arg(self):
            with self.assertRaises(TypeError):
                models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
