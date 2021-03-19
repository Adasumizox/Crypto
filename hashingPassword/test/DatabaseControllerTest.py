import os
import unittest
from hashingPassword.src.DatabaseController import DatabaseController


class DatabaseControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.databaseController = DatabaseController("test")

    def test_init(self):
        self.assertIsInstance(self.databaseController, DatabaseController)

    def test_user_creation(self):
        self.assertEqual(self.databaseController.create_user("test", "test", "test", "test"), None)

    def tearDown(self) -> None:
        self.databaseController = None
        os.remove('./test')
