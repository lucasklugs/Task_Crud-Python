from datetime import date
from task_repository import TaskRepository

class Task:
    def __init__(self, id: int, priority: str, desc: str, t_date: date, status: str):
        self.id     = id
        self.pr     = priority
        self.desc   = desc
        self.status = status
        self.date   = t_date

    def __str__(self):
        return f"{self.id}, {self.pr}, {self.desc}, {self.date}, {self.status}"

class TaskCrud:
    def __init__(self, repository):
        self.tasks = []  
        self.repository: TaskRepository = repository


    def create_table(self):
        self.repository.create_table()

    def create_task(self, priority, desc, t_date, status):
        task = Task(0, priority, desc, t_date, status)
        self.repository.insert_table(task) 
        print("Tarefa criada")

    def read_task(self):
        results = self.repository.read_table()
        if not results:
            print("Nenhuma tarefa encontrada.")
        else:
            for result in results:
                print(f"ID: {result[0]}, Prioridade: {result[1]}, Descrição: {result[2]}, Status: {result[3]}, Data Limite: {result[4]}")

    def mark_done(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.status = "concluido"
                self.repository.markdone_table(task_id)
                print("Tarefa marcada como concluida.")
                return
        print("Tarefa não encontrada...")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print("Tarefa removida")
                return
            print("Tarefa não encontrada...")

    def edit_task(self, task_id, priority, desc):
        for task in self.tasks:
            if task.id == task_id:
                task.pr = priority
                task.desc = desc
                print("Tarefa editada")
                return
            print("Tarefa não encontrada...")

# Deleta todos as tarefas com status "concluido"
    def delete_done(self): # Não precisa de paramêtros além do ponteiro, pois ele percorrerá toda a lista procurando o status
        for task in self.tasks: 
            if task.status == "concluido":
                self.tasks.remove(task)
                print("Tarefas concluidas foram excluidas")
                return
            print("Você ainda não concluiu nenhuma tarefa")

    

