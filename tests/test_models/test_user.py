#!/usr/bin/python3
"""Unit tests for the user module"""
import unittest
from models.engine.file_storage import FileStorage
from models.user import User
from models import storage
from datetime import datetime
import os


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    u = None

    def setUp(self):
        self.u = User()

    def tearDown(self):
        """ set up a clean state for running each test
            method within a test case
        """

        self.u = User()
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_attrs(self):
        """Test for User class attrs"""

        self.assertIsInstance(User.email, str)
        self.assertIsInstance(User.password, str)
        self.assertIsInstance(User.first_name, str)
        self.assertIsInstance(User.last_name, str)

    def test_init(self):
        """Test method for public instances"""

        self.assertIsInstance(self.u, User)
        self.assertIsInstance(self.u.id, str)
        self.assertIsInstance(self.u.created_at, datetime)
        self.assertIsInstance(self.u.updated_at, datetime)
        self.assertIn("{}.{}".format(type(self.u).__name__, self.u.id),
                      FileStorage._FileStorage__objects.keys())
        u2 = User(**self.u.to_dict())
        self.assertEqual(self.u.updated_at, u2.updated_at)
        u2.first_name = "John"
        u2.email = "John@gmail.com"
        u2.password = "tryhackme!"
        self.assertEqual(u2.first_name, "John")
        self.assertEqual(u2.email, "John@gmail.com")
        self.assertEqual(u2.password, "tryhackme!")

    def test_str(self):
        """Test method for str representation"""

        string = f"[{type(self.u).__name__}] ({self.u.id}) {self.u.__dict__}"
        self.assertEqual(self.u.__str__(), string)

    def test_save(self):
        """Test method for save"""

        old_dt = self.u.updated_at
        self.u.save()
        self.assertGreater(self.u.updated_at, old_dt)

    def test_to_dict(self):
        """Test method for to_dict"""

        my_dict = self.u.to_dict()
        self.assertIsInstance(my_dict, dict)
        self.assertIn('__class__', my_dict.keys())
        self.assertIsInstance(my_dict['__class__'], str)
        self.assertEqual(my_dict['__class__'], type(self.u).__name__)
        self.assertIn('created_at', my_dict.keys())
        self.assertIn('updated_at', my_dict.keys())
        self.assertIsInstance(my_dict['created_at'], str)
        self.assertIsInstance(my_dict['updated_at'], str)


if __name__ == '__main__':
    unittest.main()
