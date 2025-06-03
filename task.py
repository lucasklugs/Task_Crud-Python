from datetime import date

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
    def __init__(self):
        self.tasks = []  
        self.prox_id = 1

    def create_task(self, priority, desc, t_date, status):
        task = Task(self.prox_id, priority, desc, t_date, status)
        self.tasks.append(task)  
        self.prox_id += 1
        print("Tarefa criada")

    def read_task(self):
        if not self.tasks:
            print("Nenhuma tarefa encontrada.")
        else:
            for task in self.tasks:
                print(task)

    def mark_done(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.status = "concluido"
                print("Tarefa marcada como concluida.")
                return
            print("Tarefa não encontrada...")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print("Tarefa removida")
                return
            print("Tarefa não encontrada")

    def edit_task(self, task_id, priority, desc):
        for task in self.tasks:
            if task.id == task_id:
                task.pr = priority
                task.desc = desc
                print("Tarefa editada")
                return
            print("Tarefa não encontrada")

#Deleta todos os 
    def delete_done(self):
        for task in self.tasks:
            if task.status == "concluido":
                self.tasks.remove(task)
                print("Tarefas concluidas foram excluidas")
                return
            print("Você ainda não concluiu nenhuma tarefa")

    

