class TaskRepository:

    def __init__(self, conn):
        self.conn = conn

    def create_cursor(self):
        return self.conn.cursor()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            t_date TEXT NOT NULL
        );
        """
        cursor = self.create_cursor()
        cursor.execute(query)
        cursor.close()

    def insert_table(self, task):
        query = """
        INSERT INTO task (
            priority,
            description,
            status,
            t_date
        ) VALUES (?, ?, ?, ?);
        """
        cursor = self.create_cursor()
        result = cursor.execute(query, (task.pr, task.desc, task.status, task.date)).lastrowid
        if not result:
            print("Tarefa não incluida")
        self.conn.commit()
        cursor.close()

    
    def read_table(self):
        query = """
        SELECT id, priority, description, status, t_date FROM task;
        """
        cursor = self.create_cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # A várivel result deterá todos os itens consultados por meio do fetchall() 
        cursor.close()
        return result  # Retorna result para que a váriavel seja chamada no task.py
    
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

    def delete_table(self, task_id):
        query = "DELETE FROM task WHERE id = ?;"
        cursor = self.create_cursor()
        cursor.execute(query, (task_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa com esse ID foi encontrada.")
        else:
            print("Tarefa deletada!")
        cursor.close()

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

    def cleardone_table(self):
        query = "DELETE FROM task WHERE status = 'concluída';"
        cursor = self.create_cursor()
        cursor.execute(query)  # Sem parâmetros
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Nenhuma tarefa foi concluída.")
        else:
            print("Tarefas concluídas excluídas...")
        cursor.close()