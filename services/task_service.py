from mysql.connector import Error
from db_config import get_db_connection
from models.task import Task

class TaskService:
    """
    Handles all database interactions for Tasks using raw SQL.
    """

    def add_task(self, task):
        connection = get_db_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO tasks (title, description, due_date, priority, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (task.title, task.description, task.due_date, task.priority, task.status)
            
            cursor.execute(query, values)
            connection.commit()
            return True
            
        except Error as e:
            print(f"Error adding task: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_tasks(self, status_filter=None):
        connection = get_db_connection()
        tasks = []
        if not connection:
            return tasks

        try:
            cursor = connection.cursor(dictionary=True)
            
            if status_filter:
                query = "SELECT * FROM tasks WHERE status = %s ORDER BY due_date ASC"
                cursor.execute(query, (status_filter,))
            else:
                query = "SELECT * FROM tasks ORDER BY due_date ASC"
                cursor.execute(query)

            for row in cursor.fetchall():
                tasks.append(Task(**row)) # Unpack dictionary directly into Task object
                
        except Error as e:
            print(f"Error fetching tasks: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return tasks

    def update_task(self, task_id, title, description, due_date, priority):
        connection = get_db_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = """
                UPDATE tasks 
                SET title=%s, description=%s, due_date=%s, priority=%s 
                WHERE id=%s
            """
            cursor.execute(query, (title, description, due_date, priority, task_id))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating task: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def mark_task_complete(self, task_id):
        connection = get_db_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = "UPDATE tasks SET status='Completed' WHERE id=%s"
            cursor.execute(query, (task_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error completing task: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_task(self, task_id):
        connection = get_db_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM tasks WHERE id=%s"
            cursor.execute(query, (task_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting task: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()