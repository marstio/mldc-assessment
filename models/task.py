from datetime import datetime

class Task:
    """
    Represents a task entity.
    """
    def __init__(self, title, description, due_date, priority='Medium', status='Pending', id=None, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        """Helper to convert task to dictionary for easy display."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': str(self.due_date),
            'priority': self.priority,
            'status': self.status
        }