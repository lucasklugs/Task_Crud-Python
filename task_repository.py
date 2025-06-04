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

    
    def read_table(self, task):
        query = """
        SELECT priority, desc, status, t_date FROM task;
        """
        cursor = self.create_cursor()
        result = cursor.execute(query (task.pr, task.desc, task.status, task.date))
        
        cursor.close()
        