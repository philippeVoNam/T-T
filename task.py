 # * author : Philippe Vo 
 # * date : Jan-31-2021 21:49:05
 
# * Imports
# 3rd Party Imports
import yaml
from prompt_toolkit import prompt
# User Imports

"""
TODO :
- [ ] how to make a "refreshable" text area so that we can add to the tasks and have it update the
view live.
- [ ] find a python terminal library that will allow todo this ^
"""

# * Code
tasksFilePath = "tasks.yaml"

class TaskViewer:
    """
    class that helps with viewing tasks
    """
    def __init__(self):
        pass

    def run(self):
        quitFlag = False

        firstFlag = True
        while not quitFlag:
            self.show(firstFlag)
            firstFlag = False

            # user input
            userInput = input("")

            if userInput == "q":
                return

    def show(self, showFlag):
        if showFlag:
            th = TaskHandler()
            tasksData = th.read_tasks()
            for taskDataInfo in tasksData:
                print(th.task_print_format(taskDataInfo))

class Task:
    """
    class that represents tasks
    """
    def __init__(self, id: int, taskText: str):
        self.id = id
        self.taskText = taskText
        self.isDone = False

    def get_data(self):
        data = {
            "id": self.id,
            "taskText": self.taskText,
            "isDone": self.isDone
        }

        return data

class TaskHandler:
    """
    class that helps with handling tasks
    """
    def __init__(self):
        pass
    
    def add_task(self, task: Task): 
        """
        add task to database
        """
        if not self.task_exist(task.id):
            with open(tasksFilePath, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)

                if data != None:
                    updateData = data
                else:
                    updateData = []

                with open(tasksFilePath, 'w') as f:
                    newData = task.get_data()
                    updateData.append(newData)
                    yaml.dump(updateData, f)

    def read_tasks(self): 
        """
        read all the tasks
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            return data

    def remove_task(self, id: int): 
        """
        remove task to database
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            if data != None:
                updateData = data
            else:
                updateData = []

            # remove the task
            for taskData in updateData:
                if int(taskData["id"]) == id:
                    data.remove(taskData)

            with open(tasksFilePath, 'w') as f:
                yaml.dump(updateData, f)

    def task_exist(self, id: int):
        """
        check if task exist
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            
            if data == None:
                return False

            # update the task
            for taskData in data:
                if int(taskData["id"]) == id:
                    return True

            return False

    def set_task_status(self, id: int, status: bool): 
        """
        update task status
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            if data != None:
                updateData = data
            else:
                updateData = []

            # update the task
            for taskData in updateData:
                if int(taskData["id"]) == id:
                    taskData["isDone"] = status

            with open(tasksFilePath, 'w') as f:
                yaml.dump(updateData, f)

    def reset_database(self):
        """
        erase entire database
        """
        open(tasksFilePath, 'w').close()

    def task_print_format(self, taskData):
        """
        return a printable format of the task
        """
        if taskData["isDone"]:
            status = "X"
        else:
            status = " "

        return "{} [{}] {}".format(taskData["id"], status, taskData["taskText"])

task = Task(1, "wow")
task1 = Task(2, "wow")
th = TaskHandler()
th.add_task(task)
th.add_task(task1)
# th.read_tasks()
# th.remove_task(2)
th.set_task_status(1, True)
# th.reset_database()
tv = TaskViewer()
tv.run()
