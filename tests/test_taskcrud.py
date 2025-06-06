import unittest
from unittest.mock import Mock
from src.task import TaskCrud

class TestTaskCrud(unittest.TestCase):
    def setUp(self):
      self.repository_mock = Mock()
      self.repository_mock.insert_table.return_value = "teste"

    def test_create_task(self):
       crud = TaskCrud(self.repository_mock)
       result = crud.create_task("alta", "Teste", "2025-12-31", "teste")
       self.assertEqual(result, "teste")      