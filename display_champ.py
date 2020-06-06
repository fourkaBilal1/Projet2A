import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd


class Graph():
    def __init__(self):
        pass

    def add_data_set(self, x, y, legend=''):
        plt.plot(x, y, label=legend)
        
    def add_data_setT(self, data):
        df = pd.DataFrame(data)
        plt.quiver( 
            df.loc[:,'x'], 
            df.loc[:,'y'],
            -np.sin(df.loc[:,'theta_shifts'])*2, 
            -np.cos(df.loc[:,'theta_shifts'])*2,
            color=['r','b','g'], 
            scale= 23 )

    def show(self):
        plt.show()

    def draw(self, x, y):
        self.add_data_set(x, y)
        self.show()

    def savefig(self, name):
        plt.savefig("./logs/" + name)

    def add_legend(self, title, x, y):
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)

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
    filename = input('file name?')
    data = get_data_from_json(filename)
    
    g = Graph()
    g.add_legend("Trajectory", "x", "y")
    g.add_data_setT(data)
    g.add_data_set(data["x"], data["y"])
    
    g.show()






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
