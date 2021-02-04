 # * author : Philippe Vo 
 # * date : Jan-31-2021 21:49:05
 
# * Imports
# 3rd Party Imports
import yaml
import os
from datetime import date, datetime
from progress.bar import ChargingBar
# User Imports

"""
TODO :
- [ ] reset at the start of new day
- [ ] fix ID issue -> instead of looking at len(of id) -> we need to get largest num of ID (is max ID) and add + 1 to get new id 
"""

# * Code
tasksFilePath = "/home/namv/Documents/Personal_Projects/T-T/tasks.yaml"
updateDateFilePath = "/home/namv/Documents/Personal_Projects/T-T/update_date.txt"

class TaskViewer:
    """
    class that helps with viewing tasks
    """
    def __init__(self):
        pass

    def run(self):
        quitFlag = False
        firstFlag = True

        today = date.today()
        th = TaskHandler()
        mostRecentUpdateDateStr = th.read_date()
        mostRecentUpdateDate = datetime.strptime(mostRecentUpdateDateStr, "%d/%m/%Y").date()

        if mostRecentUpdateDate < today:
            # new day == reset database
            th.reset_database()

        th.update_date()

        self.clear_view()
        while not quitFlag:
            self.show(firstFlag)
            firstFlag = False

            # user input
            userInput = input("cmd (a/r/t/q) : ")
            userInputChar = userInput[0]

            if userInputChar == "q" and len(userInput) == 1:
                return
            
            elif userInputChar == "a" and len(userInput) == 1:
                taskText = input("task : ")
                th = TaskHandler()
                newID = th.get_max_id() + 1
                task = Task(newID, taskText)
                th.add_task(task)

                self.reset_view()

            elif userInputChar == "t":
                try:
                    taskID = self.get_id(userInput)
                    th = TaskHandler()

                    if taskID > th.get_max_id() or taskID < 1:
                        print("invalid id")

                    else:
                        th.toggle_task_status(taskID)

                except (TypeError, ValueError):
                    print("invalid cmd")

                finally:
                    self.reset_view()

            elif userInputChar == "r":
                try:
                    taskID = self.get_id(userInput)
                    th = TaskHandler()

                    if taskID > th.get_max_id() or taskID < 1:
                        print("invalid id")

                    else:
                        th.remove_task(taskID)

                except (TypeError, ValueError):
                    print("invalid cmd")

                finally:
                    self.reset_view()

            else:
                self.reset_view()

    def show(self, showFlag):
        if showFlag:
            th = TaskHandler()
            tasksData = th.read_tasks()

            bar = ChargingBar('', max=len(tasksData))
            for i in range(th.get_num_tasks_done()):
                bar.next()

            print("")
            print("")

            for taskDataInfo in tasksData:
                print(th.task_print_format(taskDataInfo))

            print("")

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

    def update_date(self):
        today = date.today()
        dt = today.strftime("%d/%m/%Y")

        with open(updateDateFilePath, 'w') as f:
            f.write(dt)

    def read_date(self):
        with open(updateDateFilePath, 'r') as f:
            dateStr = f.read()

            return dateStr
    
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

    def get_max_id(self): 
        """
        read all the tasks
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            maxID = 0
            for taskData in data:
                if int(taskData["id"]) > maxID:
                    maxID = int(taskData["id"])

            return maxID

    def get_num_tasks_done(self): 
        """
        read all the tasks
        """
        with open(tasksFilePath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            count = 0
            for taskData in data:
                if int(taskData["isDone"]) == True:
                    count = count + 1

            return count

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
        with open(tasksFilePath, 'w') as f:
            f.write("[]")

    def task_print_format(self, taskData):
        """
        return a printable format of the task
        """
        if taskData["isDone"]:
            status = "X"
        else:
            status = " "

        return "{} [{}] {}".format(taskData["id"], status, taskData["taskText"])

tv = TaskViewer()
tv.run()
