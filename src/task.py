from datetime import datetime, date
from task_repository import TaskRepository
import streamlit as st

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
            st.warning("Não há tarefas no banco...")
        else:
            for task in tasks:
                with st.expander(f"Tarefa ID: {task[0]}"):  
                    st.write(f"**Prioridade:** {task[1]}")
                    st.write(f"**Task:** {task[2]}")
                    st.write(f"**Status:** {task[3]}")
                    st.write(f"**Prazo:** {task[4]}")
    
    def get_pending_descriptions(self):
        return self.repository.get_pending_descriptions()

    def get_all_descriptions(self):
        return self.repository.get_all_descriptions()

    def mark_done_by_description(self, description):
        self.repository.markdone_by_description(description)

    def edit_task(self, actual_task, ed_priority, ed_desc, ed_dead):
        self.repository.edit_table(ed_priority, ed_desc, ed_dead, actual_task)

    def delete_task(self, task_desc):
        self.repository.delete_table(task_desc)

    def today_tasks(self):
        today = datetime.today().date().isoformat()
        tasks = self.repository.get_today_tasks(today)

        if not tasks:
            st.info(f"Nenhuma tarefa para hoje 😜")
            return
        
        for task in tasks:
            with st.container(border=True):  # Cria um container com borda para cada tarefa
                st.write(f"**Task:** {task[2]} | **Status:** {task[3]}")
    
    def deadline_task(self):
        tasks = self.repository.get_all_tasks_ordered_by_date()
        if not tasks:
            st.info("Não há tarefas no banco...")
            return

        datas_vistas = set()
        for task in tasks:
            deadline = task[4]  # Atribue os dados de data que estão na quarta posição do select na váriavel deadline
            if deadline not in datas_vistas:
                st.subheader(f"\n Prazo de Entrega: {deadline}")
                datas_vistas.add(deadline)
            with st.container(border=True):  # Cria um container com borda para cada tarefa
                st.write(f"**Task:** {task[2]} | **Status:** {task[3]}")


    def delete_done(self):
        self.repository.cleardone_table()

    

