class Project:
    def __init__(self, name, completion=0, status='Open'):
        self.name = name
        self.completion = completion
        self.status = status
        self.subtasks = []

    def __str__(self):
        return f"{self.name} (Completion: {self.completion}%, Status: {self.status})"


# Subtask Class (inherits from Project)
class Subtask(Project):
    def __init__(self, project_name, task_name, task_completion=0):
        super().__init__(task_name, task_completion)
        self.project = project_name

    def __str__(self):
        return f"{self.task_name} (Parent Project: {self.project.name}, Completion: {self.completion}%)"


