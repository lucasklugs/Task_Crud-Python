import unittest
from unittest.mock import Mock
from src.task_repository import TaskRepository, TaskRepositoryException

class TestTaskRepository(unittest.TestCase):
    def setUp(self):
        # Cria objetos mock para o banco de dados e cursor
        self.conn = Mock()
        self.cursor = Mock()
        self.conn.cursor.return_value = self.cursor
        # Instancia o repositório com a conexão mockada
        self.repository = TaskRepository(self.conn)

    def test_insert_table(self):
        # Testa inserção bem-sucedida no banco
        task = Mock(pr="alta", desc="Teste", status="Pendente", date="2025-12-31")
        self.cursor.execute.return_value.lastrowid = 1  # Simula retorno do ID inserido
        result = self.repository.insert_table(task)
        self.assertEqual(result, 1)  # Verifica se o ID retornado é 1
        self.conn.commit.assert_called_once()  # Confirma que commit foi chamado
        self.cursor.close.assert_called_once()  # Confirma que o cursor foi fechado

    def test_insert_table_with_taskrepositoryexception(self):
        # Testa se o método lida corretamente com inserção sem retorno de ID
        task = Mock(pr="alta", desc="Teste", status="Pendente", date="2025-12-31")
        self.cursor.execute.return_value.lastrowid = None  # Nenhuma linha inserida
        result = self.repository.insert_table(task)
        self.assertEqual(result, "Tarefa não incluida")  # Espera mensagem de erro específica

    def test_insert_table_with_exception(self):
        # Testa tratamento de exceção genérica ao tentar inserir
        task = Mock(pr="alta", desc="Teste", status="Pendente", date="2025-12-31")
        self.cursor.execute.side_effect = ValueError("Erro de conexão no banco")
        result = self.repository.insert_table(task)
        self.assertEqual(result, "Erro inesperado: Erro de conexão no banco")  # Verifica erro genérico

    def test_fetch_all(self):
        # Testa recuperação de todas as tarefas do banco
        expected = [(1, 'alta', 'desc', 'Pendente', '2025-12-31')]
        self.cursor.fetchall.return_value = expected
        result = self.repository.fetch_all()
        self.assertEqual(result, expected)  # Verifica se os dados retornados são os esperados
        self.cursor.execute.assert_called_once()  # Confirma que a query foi executada
        self.cursor.close.assert_called_once()  # Confirma que o cursor foi fechado

    def test_fetch_all_with_exception(self):
        # Testa tratamento de erro ao buscar todas as tarefas
        self.cursor.execute.side_effect = ValueError("Erro de conexão no banco")
        result = self.repository.fetch_all()
        self.assertEqual(result, "Erro inesperado: Erro de conexão no banco")

    def test_get_pending_descriptions(self):
        # Testa recuperação de descrições de tarefas pendentes
        self.cursor.fetchall.return_value = [("Tarefa 1",), ("Tarefa 2",)]
        result = self.repository.get_pending_descriptions()
        self.assertEqual(result, ["Tarefa 1", "Tarefa 2"])  # Verifica se converte para lista simples

    def test_get_pending_descriptions_with_exception(self):
        # Testa erro ao buscar descrições pendentes (OBS: está chamando fetch_all errado!)
        self.cursor.execute.side_effect = ValueError("Erro de conexão no banco")
        result = self.repository.get_pending_descriptions()
        self.assertEqual(result, "Erro inesperado: Erro de conexão no banco")

    def test_markdone_by_description(self):
        # Testa marcação de tarefa como concluída com sucesso
        self.cursor.execute.return_value.rowcount = 1  # Simula sucesso na atualização
        result = self.repository.markdone_by_description("Tarefa 1")
        self.conn.commit.assert_called_once()
        self.cursor.close.assert_called_once()
        self.assertIsNone(result)  # Método não retorna nada em caso de sucesso

    def test_markdone_by_description_with_taskrepositoryexception(self):
        # Testa falha ao tentar marcar tarefa inexistente como concluída
        self.cursor.rowcount = 0  # Simula que nenhuma linha foi afetada
        result = self.repository.markdone_by_description("Tarefa Inexistente")
        self.assertEqual(result, "Tarefa não encontrada.")

    def test_markdone_by_description_with_exception(self):
        # Testa erro inesperado ao tentar marcar tarefa como concluída
        self.cursor.execute.side_effect = ValueError("Erro de conexão no banco")
        result = self.repository.markdone_by_description("Tarefa 1")
        self.assertEqual(result, "Erro inesperado: Erro de conexão no banco")

    def test_edit_table(self):
        self.cursor.rowcount = 1
        result = self.repository.edit_table("alta", "nova desc", "2025-12-31", "desc atual")
        self.conn.commit.assert_called_once()
        self.cursor.close.assert_called_once()
        self.assertEqual(result, "Tarefa editada.")

    def test_edit_table_with_exception(self):
        self.cursor.execute.side_effect = ValueError("Erro ao editar")
        result = self.repository.edit_table("baixa", "Nova tarefa", "2025-12-31", "Tarefa")
        self.assertEqual(result, "Erro inesperado: Erro ao editar")

    def test_edit_table_with_taskrepositoryexception(self):
        self.cursor.rowcount = 0
        result = self.repository.edit_table("alta", "nova desc", "2025-12-31", "desc inexistente")
        self.assertEqual(result, "Tarefa não encontrada.")

    def test_delete_table(self):
        self.cursor.rowcount = 1
        result = self.repository.delete_table("desc")
        self.conn.commit.assert_called_once()
        self.cursor.close.assert_called_once()
        self.assertEqual(result, "Tarefa removida!")

    def test_delete_table_with_taskrepositoryexception(self):
        self.cursor.rowcount = 0 
        result = self.repository.delete_table("inexistente")
        self.assertEqual(result, "Tarefa não encontrada.")

    def test_delete_table_with_exception(self):
        self.cursor.execute.side_effect = ValueError("Erro ao deletar")
        result = self.repository.delete_table("Tarefa")
        self.assertEqual(result, "Erro inesperado: Erro ao deletar")

    def test_get_today_tasks(self):
        today = "2025-12-31"
        expected = [(1, "alta", "desc", "Pendente", today)]
        self.cursor.fetchall.return_value = expected
        result = self.repository.get_today_tasks(today)
        self.assertEqual(result, expected)

    def test_get_today_tasks_with_exception(self):
        self.cursor.execute.side_effect = ValueError("Erro ao buscar tarefas")
        result = self.repository.get_today_tasks("2025-12-31")
        self.assertEqual(result, "Erro inesperado: Erro ao buscar tarefas")
