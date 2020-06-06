import matplotlib.pyplot as mp
import json
#import Tkinter as tk
try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk
#import tkFileDialog as filedialog
#from tkinter import filedialog
from tkinter import filedialog
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Graph():
    def __init__(self):
        pass

    def add_data_set(self, x, y, legend=''):
        mp.plot(x, y, label=legend)
        
    def add_data_setT(self, data):
        df = pd.DataFrame(data)
        plt.quiver( 
            df.loc[:,'x'], 
            df.loc[:,'y'],
            -np.sin(df.loc[:,'theta'])*2, 
            -np.cos(df.loc[:,'theta'])*2,
            color=['r','b','g'], 
            scale= 23 )
        
    def add_data_setTs(self, data):
        df = pd.DataFrame(data)
        plt.quiver( 
            df.loc[:,'x'], 
            df.loc[:,'y'],
            -np.sin(df.loc[:,'theta_shifts'])*2, 
            -np.cos(df.loc[:,'theta_shifts'])*2,
            color=['r','b','g'], 
            scale= 23 )
        
    def show(self):
        mp.show()

    def draw(self, x, y):
        self.add_data_set(x, y)
        self.show()

    def savefig(self, name):
        mp.savefig("./logs/" + name)

    def add_legend(self, title, x, y):
        mp.title(title)
        mp.xlabel(x)
        mp.ylabel(y)

def draw_from_set(x, y):
    graph = Graph()
    graph.draw(x, y)

def draw_from_file(name):
    with open(name) as f:
        data = json.load(f)
        graph = Graph()
        graph.add_data_set([p[0] for p in data["positions"]], [p[1] for p in data["positions"]])
        #graph.draw()

def get_data_from_json(name):
    new_data = {}
    with open(name) as f:
        data = json.load(f)
        new_data["size"] = data["size"]
        new_data["t"] = data["times"]
        new_data["x"]= [p[0] for p in data["positions"]]
        new_data["y"] = [p[1] for p in data["positions"]]
        new_data["theta"] = [p[2] for p in data["positions"]]
        new_data["theta_shifts"] = data["theta_shifts"]
        new_data["criterions"] = data["criterions"]
        new_data["q1"] = [p[0] for p in data["commands"]]
        new_data["q2"] = [p[1] for p in data["commands"]]
        return new_data

if __name__ == "__main__":
#    print("here i am 1")
    root = tk.Tk()
    root.withdraw()
#    print("here i am 2")
#    filename = filedialog.askopenfilename(initialdir = "logs/",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
    filename = input('file name?')
#    print("here i am 3")
    root.update()
#    print("\n\n")
#    print(filename)
#    print("\n\n")
    data = get_data_from_json(filename)

#    #Compared graphics initialization : uncomment and specify the directory of lessons and tests you want to print
#    directory = 'rapport_thetat_sans_random'
#
#    data1 = get_data_from_json('./logs/' + directory + '/lesson1.json')
#    data2 = get_data_from_json('./logs/' + directory + '/lesson2.json')
#    data3 = get_data_from_json('./logs/' + directory + '/lesson3.json')
#
#    test1 = get_data_from_json('./logs/' + directory + '/test1.json')
#    test2 = get_data_from_json('./logs/' + directory + '/test2.json')
#    test3 = get_data_from_json('./logs/' + directory + '/test3.json')
#    test4 = get_data_from_json('./logs/' + directory + '/test4.json')
#    test5 = get_data_from_json('./logs/' + directory + '/test5.json')

#    print("Parameters:\n" +
#          "- Size of the training area: " + str(data["size"]))

    g = Graph()
    g.add_legend("Trajectory", "x", "y")
    g.add_data_set(data["x"], data["y"])
    g.show()

    g = Graph()
    g.add_legend("Evolution of x(t)", "t", "x")
    g.add_data_set(data["t"], data["x"])
    g.show()

    g = Graph()
    g.add_legend("Evolution of y(t)", "t", "y")
    g.add_data_set(data["t"], data["y"])
    g.show()

    g = Graph()
    g.add_legend("Evolution of theta(t)", "t", "theta")
    g.add_data_set(data["t"], data["theta"])
    g.show()

    g = Graph()
    g.add_legend("Vector field of theta", "x", "y")
    g.add_data_setT(data)
    g.add_data_set(data["x"], data["y"])
    g.show()
    
    g = Graph()
    g.add_legend("Evolution of theta_shift(t)", "t", "theta_shift")
    g.add_data_set(data["t"], data["theta_shifts"])
    g.show()

    g = Graph()
    g.add_legend("Vector field of theta_shift", "x", "y")
    g.add_data_setTs(data)
    g.add_data_set(data["x"], data["y"])
    g.show()
    
    g = Graph()
    g.add_legend("Evolution of criterion(t)", "t", "criterion")
    g.add_data_set(data["t"], data["criterions"])
    g.show()

    g = Graph()
    g.add_legend("Evolution of q1(t)", "t", "q1")
    g.add_data_set(data["t"], data["q1"])
    g.show()

    g = Graph()
    g.add_legend("Evolution of q2(t)", "t", "q2")
    g.add_data_set(data["t"], data["q2"])
    g.show()

    
#    #Compared graphics
#    g = Graph()
#    g.add_legend("Compared trajectories of lessons", "x", "y")
#    g.add_data_set(data1["x"], data1["y"], 'lesson 1')
#    g.add_data_set(data2["x"], data2["y"], 'lesson 2')
#    g.add_data_set(data3["x"], data3["y"], 'lesson 3')
#    mp.legend()
#    g.show()
#
#    g = Graph()
#    g.add_legend("Compared trajectories of tests", "x", "y")
#    g.add_data_set(test1["x"], test1["y"], 'test 1')
#    g.add_data_set(test2["x"], test2["y"], 'test 2')
#    g.add_data_set(test3["x"], test3["y"], 'test 3')
#    g.add_data_set(test4["x"], test4["y"], 'test 4')
#    mp.legend()
#    g.show()
#
#
#    g = Graph()
#    g.add_legend("Failing test", "x", "y")
#    g.add_data_set(test5["x"], test5["y"], 'test 5')
#    mp.legend()
#    g.show()
