#!/usr/bin/python3
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
from datetime import datetime


class TestBasemodel(unittest.TestCase):
    """Test cases for the Basemodel class"""

    b = None

    def setUp(self):
        """ set up a clean state for running each test
            method within a test case
        """
        self.b = BaseModel()

    def tearDown(self):
        """clean up after each test method has executed"""

        self.b = BaseModel()
        FileStorage._FileStorage__objects = {}
        path = FileStorage._FileStorage__file_path
        if os.path.exists(path):
            os.remove(path)

    def test_initialization(self):
        """Test of initialization of basemodel"""

        self.assertIsInstance(self.b, BaseModel)
        self.assertIsInstance(self.b.id, str)
        self.assertIsInstance(self.b.created_at, datetime)
        self.assertIsInstance(self.b.updated_at, datetime)
        my_dict = self.b.to_dict()
        self.assertEqual(my_dict['__class__'], "BaseModel")
        self.assertIsInstance(my_dict['created_at'], str)
        self.assertIsInstance(my_dict['updated_at'], str)
        b2 = BaseModel(**my_dict)
        self.assertIsInstance(b2, BaseModel)
        self.assertEqual(b2.__class__, BaseModel)
        self.assertIsInstance(b2.created_at, datetime)
        self.assertIsInstance(b2.updated_at, datetime)
        b2.my_name = "John"
        b2.my_age = 30
        self.assertEqual(b2.my_name, "John")
        self.assertIsInstance(b2.my_name, str)
        self.assertEqual(b2.my_age, 30)
        self.assertIsInstance(b2.my_age, int)

    def test_str(self):
        """Test method for __str__"""

        s = self.b.__str__()
        self.assertIsInstance(s, str)
        f = "[{}] ({}) {}".format(type(self.b). __name__,
                                  self.b.id, self.b.__dict__)
        self.assertEqual(s, f)

    def test_to_dict(self):
        """Test method for to_dict"""

        my_dict = self.b.to_dict()
        self.assertIsInstance(my_dict, dict)
        self.assertIn('__class__', my_dict.keys())
        self.assertIsInstance(my_dict['__class__'], str)
        self.assertEqual(my_dict['__class__'], type(self.b).__name__)
        self.assertIn('created_at', my_dict.keys())
        self.assertIn('updated_at', my_dict.keys())
        self.assertIsInstance(my_dict['created_at'], str)
        self.assertIsInstance(my_dict['updated_at'], str)

    def test_save(self):
        """Test method for save"""

        old_dt = self.b.updated_at
        self.b.save()
        self.assertGreater(self.b.updated_at, old_dt)

    
    def test_one_save(self):
        """Test for save method"""
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_two_saves(self):
        """Test for save method"""
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        """Test for save method"""
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)


if __name__ == '__main__':
    unittest.main()
