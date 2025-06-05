from datetime import datetime, date
from task_repository import TaskRepository

#Cria constante de mensagem repetitiva 
MSG_NO_TASKS = "Nenhuma tarefa encontrada..."

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
        tasks = self.repository.fetch_all() # Recebe todos os dados consultados pela query
        if not tasks:
            print(MSG_NO_TASKS)
        else:
            for task in tasks:
                print(f"ID: {task[0]}, Prioridade: {task[1]}, Descrição: {task[2]}, Status: {task[3]}, Prazo de entrega: {task[4]}")

    def mark_done(self, task_id):
        self.repository.markdone_table(task_id)

    def delete_task(self, task_id):
        self.repository.delete_table(task_id)

    def edit_task(self, priority, desc, task_id):
        self.repository.edit_table(priority, desc, task_id)

    def today_tasks(self):
        today = datetime.today().date().isoformat()
        tasks = self.repository.get_today_tasks(today)

        if not tasks:
            print("Nenhuma tarefa para hoje ;) ")
            return
        
        print(f"Tarefas para hoje:")
        for task in tasks:
            print(f"- Task: {task[2]}, Status: {task[3]}")
    
    def deadline_task(self):
        tasks = self.repository.get_all_tasks_ordered_by_date()
        if not tasks:
            print(MSG_NO_TASKS)
            return

        datas_vistas = set()
        for task in tasks:
            deadline = task[4]  # Atribue os dados de data que estão na quarta posição do select na váriavel deadline
            if deadline not in datas_vistas:
                print(f"\n Prazo de Entrega: {deadline}")
                datas_vistas.add(deadline)
            print(f"- Prioridade: {task[1]}, Descrição: {task[2]}, Status: {task[3]}")


    def delete_done(self):
        self.repository.cleardone_table()

    

