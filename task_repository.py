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
        cursor = self.create_cursor()
        result = cursor.execute(query, (task.pr, task.desc, task.status, task.date)).lastrowid
        if not result:
            print("Tarefa não incluida")
        self.conn.commit()
        cursor.close()

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
    
    # Ação update para atualizar tasks para "concluída"
    def markdone_table(self, task_id):
        query = "UPDATE task SET status = 'concluída' WHERE id = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (task_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa com esse ID foi encontrada.")
        else:
            print("Tarefa marcada como concluída.")
        cursor.close()

    # Ação delete para remover tasks específicas
    def delete_table(self, task_id):
        query = "DELETE FROM task WHERE id = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (task_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa com esse ID foi encontrada.")
        else:
            print("Tarefa removida!")
        cursor.close()

    # Ação update para editar prioridade e descrição
    def edit_table(self, priority, desc, task_id):
        query = "UPDATE task SET priority = ?, description = ? WHERE id = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (priority, desc, task_id))
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa com esse ID foi encontrada.")
        else:
            print("Tarefa editada.")
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
        query = "DELETE FROM task WHERE status = 'concluída';"
        cursor = self.create_cursor()
        cursor.execute(query)  
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa foi concluída.")
        else:
            print("Tarefas concluídas excluídas...")
        cursor.close()