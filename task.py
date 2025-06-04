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
        results = self.repository.fetch_all() # Recebe todos os dados que es
        if not results:
            print("Nenhuma tarefa encontrada.")
        else:
            for result in results:
                print(f"ID: {result[0]}, Prioridade: {result[1]}, Descrição: {result[2]}, Status: {result[3]}, Data Limite: {result[4]}")

    def mark_done(self, task_id):
        self.repository.markdone_table(task_id)

    def delete_task(self, task_id):
        self.repository.delete_table(task_id)

    def edit_task(self, priority, desc, task_id):
        self.repository.edit_table(priority, desc, task_id)

    def delete_done(self):
        self.repository.cleardone_table()

    

