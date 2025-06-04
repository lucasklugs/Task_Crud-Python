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
            desc TEXT NOT NULL,
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
            desc,
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
        SELECT id, priority, desc, status, t_date FROM task;
        """
        cursor = self.create_cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # A várivel result deterá todos os itens consultados por meio do fetchall() 
        cursor.close()
        return result  # Retorna result para que a váriavel seja chamada no task.py
    
    def markdone_table(self, task_id):
        query = """
        UPDATE task
        SET status = 'concluido'
        WHERE id = ?; 
        """
        cursor = self.create_cursor()
        cursor.execute(query, (task_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            print("Tarefa não encontrada ou status não alterado")
        cursor.close()