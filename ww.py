 # * author : Philippe Vo 
 # * date : Feb-06-2021 22:13:21
 
# * Imports
# 3rd Party Imports
from datetime import date, datetime
# import plotext as plt
import matplotlib.pyplot as plt
import csv
# User Imports

# * Code
# GLOBALS
weightFilePath = "weight_data.csv"
updateDateFilePath = "/home/namv/Documents/Personal_Projects/W-W/update_date.txt"

class WeightViewer():
    """
    class that helps with viewing the graph
    """
    def __init__(self):
        """ init. """
        pass

    def run(self):
        quitFlag = False
        firstFlag = True

        today = date.today()
        wh = WeightFileHandler()
        mostRecentUpdateDateStr = wh.read_date()
        mostRecentUpdateDate = datetime.strptime(mostRecentUpdateDateStr, "%d/%m/%Y").date()

        if mostRecentUpdateDate < today:
            # new day == reset database
            self.add_weight()

        wh.update_date()

        self.show_weight_graph()

    def add_weight(self):
        wh = WeightFileHandler()
        weight = float(input("add weight : "))

        wh.add_weight(weight)

    def show_weight_graph(self):
        wh = WeightFileHandler()
        days, weights = wh.read_weights()
        # plt.plot(weights)
        # plt.ylabel('weight (kg)')
        # plt.show()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim(0,100)
        x = list(range(len(weights)))
        plt.plot(x, weights)
        for i,j in zip(x, weights):
            ax.annotate(str(j),xy=(i,j))

        plt.show()

class WeightFileHandler():
    """
    class that handles the weight data write/readd into csv file
    """
    def __init__(self):
        """ init. """
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

    def add_weight(self, weight: float):
        """
        write weight of the day to weight file
        """
        today = date.today()
        dt = today.strftime("%d.%m.%Y")

        data = [dt, weight]
        with open(weightFilePath,'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def read_weights(self):
        days = []
        weights = []
        # reading csv file 
        with open(weightFilePath, 'r') as f: 
            csvreader = csv.reader(f) 
            # extracting each data row one by one 
            for row in csvreader: 
                days.append(row[0]) 
                weights.append(row[1]) 

            weights = list(map(float, weights))
            # days = map(float, days)

            return days, weights
