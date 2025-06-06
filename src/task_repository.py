import streamlit as st

class TaskRepository:

    def __init__(self, conn):
        self.conn = conn

    # Cria o CURSOR que executa os comandos SQL dentro do SQLite
    def create_cursor(self):
        return self.conn.cursor()

    # Ação create para criar os campos
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline TEXT NOT NULL
        );
        """
        cursor = self.create_cursor()
        cursor.execute(query)
        cursor.close()

    # Ação insert para criar tasks
    def insert_table(self, task):
        query = """
        INSERT INTO task (
            priority,
            description,
            status,
            deadline
        ) VALUES (?, ?, ?, ?);
        """

        try:
            cursor = self.create_cursor()
            result = cursor.execute(query, (task.pr, task.desc, task.status, task.date)).lastrowid
            if not result:
                print("Tarefa não incluida")
            self.conn.commit()
            cursor.close()
            return result
        except Exception as e:
            st.info(e)

    # Ação select para listar todos os campos do banco   
    def fetch_all(self):
        query = """
        SELECT id, priority, description, status, deadline FROM task;
        """
        cursor = self.create_cursor()
        cursor.execute(query)
        task = cursor.fetchall()  # A várivel result deterá todos os dados consultados por meio do fetchall() 
        cursor.close()
        return task  # Retorna result para que a váriavel seja chamada no task.py
    
    def get_pending_descriptions(self):
        query = "SELECT description FROM task WHERE status != 'Concluída';"
        cursor = self.create_cursor()
        cursor.execute(query)
        descriptions = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return descriptions

    # Ação update para atualizar tasks para "concluída"
    def markdone_by_description(self, description):
        query = "UPDATE task SET status = 'Concluída' WHERE description = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (description,))
        self.conn.commit()
        if cursor.rowcount == 0:
            st.warning("Tarefa não encontrada.")
        else:
            st.success("Tarefa marcada como concluída!")
        cursor.close()

    def get_all_descriptions(self):
        query = "SELECT description FROM task"
        cursor = self.create_cursor()
        cursor.execute(query)
        descriptions = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return descriptions
    
    # Ação update para editar prioridade, descrição e data
    def edit_table(self, ed_priority, ed_desc, ed_dead, actual_task):
        query = "UPDATE task SET priority = ?, description = ?, deadline = ? WHERE description = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, ( ed_priority, ed_desc, ed_dead, actual_task))
        self.conn.commit()
        if cursor.rowcount == 0:
            st.warning("Tarefa não encontrada.")
        else:
            st.success("Tarefa editada.")
        cursor.close()

    # Ação delete para remover tasks específicas
    def delete_table(self, task_desc):
        query = "DELETE FROM task WHERE description = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (task_desc,))
        self.conn.commit()
        if cursor.rowcount == 0:
            st.warning("Nenhuma tarefa com essa descrição foi encontrada.")
        else:
            st.success("Tarefa removida!")
        cursor.close()
    

    # Ação select para listar as tarefas de hoje
    def get_today_tasks(self, date_str):
        query = "SELECT id, priority, description, status, deadline FROM task WHERE deadline = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (date_str,))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    # Ação select para listar as tarefas por data
    def get_all_tasks_ordered_by_date(self):
        query = "SELECT id, priority, description, status, deadline FROM task ORDER BY deadline ASC"
        cursor = self.create_cursor()
        cursor.execute(query)
        task = cursor.fetchall()
        cursor.close()
        return task

    # Ação delete para remover tarefas já concluídas
    def cleardone_table(self):
        query = "DELETE FROM task WHERE status = 'Concluída';"
        cursor = self.create_cursor()
        cursor.execute(query)  
        self.conn.commit()
        if cursor.rowcount == 0:
            st.warning("Nenhuma tarefa foi concluída.")
        else:
            st.success("Tarefas concluídas excluídas...")
        cursor.close()
