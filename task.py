 # * author : Philippe Vo 
 # * date : Jan-31-2021 21:49:05
 
# * Imports
# 3rd Party Imports
import yaml
import os
from prompt_toolkit import prompt
# User Imports

"""
TODO :
- [ ] reset at the start of new day
- [ ] fix ID issue -> instead of looking at len(of id) -> we need to get largest num of ID (is max ID) and add + 1 to get new id 
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

        self.clear_view()
        while not quitFlag:
            self.show(firstFlag)
            firstFlag = False

            # user input
            userInput = input("cmd (a/r/t/q) : ")
            userInputChar = userInput[0]

            if userInputChar == "q":
                return
            
            elif userInputChar == "a":
                taskText = input("task : ")
                th = TaskHandler()
                newID = th.len_tasks() + 1
                task = Task(newID, taskText)
                th.add_task(task)

                self.reset_view()

            elif userInputChar == "t":
                taskID = self.get_id(userInput)
                th = TaskHandler()

                if taskID > th.len_tasks() or taskID < 1:
                    print("invalid id")

                else:
                    th.toggle_task_status(taskID)

                self.reset_view()

            elif userInputChar == "r":
                taskID = self.get_id(userInput)
                th = TaskHandler()

                if taskID > th.len_tasks() or taskID < 1:
                    print("invalid id")

                else:
                    th.remove_task(taskID)

                # self.reset_view()

    def show(self, showFlag):
        if showFlag:
            th = TaskHandler()
            tasksData = th.read_tasks()
            for taskDataInfo in tasksData:
                print(th.task_print_format(taskDataInfo))

    def clear_view(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def reset_view(self):
        self.clear_view()
        self.show(True)

    def get_id(self, userInput):
        num = int(userInput[1:])
        return num

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
            data.sort(key = lambda x: x["id"])

            return data

    def len_tasks(self): 
        """
        read all the tasks
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            return len(data)

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

    def toggle_task_status(self, id: int): 
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
                    taskData["isDone"] = not taskData["isDone"]

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
# th.reset_database()
tv = TaskViewer()
tv.run()
