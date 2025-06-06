import unittest
from unittest.mock import Mock
from src.task_repository import TaskRepository

class TestTaskRepository(unittest.TestCase):
    def setUp(self):
        self.conn = Mock()
        self.conn.cursor.return_value = Mock()
        self.conn.cursor.execute.return_value = Mock()
        self.conn.cursor.execute.lastrowid.return_value = 1

        self.task = Mock()
        self.task.pr.return_value = "teste"
        self.task.desc.return_value = "teste"
        self.task.status.return_value = "teste"
        self.task.date.return_value = "teste"

    def test_insert_table(self):
        repository = TaskRepository(self.conn)
        result = repository.insert_table(self.task)
        self.assertEqual(result, 1)
