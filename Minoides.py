# -*- coding: utf-8 -*-

"""
Code pour remplacer run sous forme d'application graphique dans le projet
Minoïde.

"""

import threading
from Tkinter import Button
from Tkinter import Tk
from Tkinter import Label
from Tkinter import Entry
#from Tkinter import Messagebox
from Tkinter import Checkbutton
from Tkinter import BooleanVar
from BackProp_Python_v2 import NN
from vrep_pioneer_simulation import VrepPioneerSimulation
from rdn import Pioneer # rdn pour ROS avec le pioneer
import rospy
from online_trainer import OnlineTrainer
import json

class Interface():
    def __init__(self, init, speed):
        self.init_compt = init
        self.speed = speed

        self.window = Tk()
        self.title = self.window.title('IA Minoïde')
        self.window.geometry('500x200')

        self.lbl = Label(self.window)
        self.btn = Button(self.window)

        self.reinit()

        self.window.mainloop()

    def start(self):
        net = self.NETWORK.get()
        chk1 = self.chk_state1.get()
        try:
            value0 = int(self.txt1.get())
            value1 = int(self.txt2.get())
            value2 = int(self.txt3.get())
            self.terget = [value0, value1, value2]
        except:
            #Messagebox.showinfo('Attention/',
                                #'Les valeurs entrées ne sont pas correctes !')
            return
        self.txt1.destroy()
        self.txt2.destroy()
        self.txt3.destroy()
        self.chk0.destroy()
        self.chk1.destroy()
        self.res = 'Coordonnées cible: ('\
            + str(value0) + ', ' + str(value1)\
            +", "+ str(value2) + ')'

        #robot = VrepPioneerSimulation()
        robot = Pioneer(rospy)
        HL_size= 10# nbre neurons of Hiden layer
        network = NN(3, HL_size, 2)
        self.trainer = OnlineTrainer(robot, network)

        if net:
            with open('last_w.json') as fp:
                json_obj = json.load(fp)
            for i in range(3):
                for j in range(HL_size):
                    network.wi[i][j] = json_obj["input_weights"][i][j]
            for i in range(HL_size):
                for j in range(2):
                    network.wo[i][j] = json_obj["output_weights"][i][j]
            print('Check 0 True')
        else:
            print('Check 0 False')

        if chk1:
            print('Check 1 True')
            thread = threading.Thread(target=self.trainer.train, args=(self.terget,))
            thread.start()
        else:
            print('Check 1 False')

        if net:
            self.window.after(1, self.loop)
        else:
            self.window.after(1, self.save_file)

    def save_file(self):
        self.txt = Entry(self.window, width=30)
        self.lbl.config(text='Give a name to the log file (default to last):')
        self.btn.config(text='Valider', command=self.loop)

        self.txt.grid(column=0, row=1)
        self.lbl.grid(column=0, row=0)
        self.btn.grid(column=0, row=2)

        try:
            self.file_name = self.txt.get()
        except:
            """Messagebox.showinfo('Attention/',
                                "Le nom de fichier n'est pas correct")"""
        if self.file_name == '':
            self.file_name = 'last'
        with open("logs/" + self.file_name + ".json", 'w') as f:
	    print(self.trainer.log_file)
            json.dump(self.trainer.log_file, f)
        f.close()
        print('Graph values have been saved in ' + self.file_name +'.json file')

    def loop(self):

        self.lbl.config(text=self.res)
        self.btn.config(text='Stop', command=self.stop)
        try:
            self.txt.destroy()
        except:
            pass

        if self.arret == 1:
            self.arret = 0
            self.lbl.config(text='Arrêt')
            self.btn.config(text='Réinitialiser', command=self.reinit)
            return

        if self.compt <= 0:
            self.lbl.config(text='Time is over !')
            self.btn.config(text='Réinitialiser', command=self.reinit)
            return

        self.compt -= self.speed/100

        self.window.after(1, self.loop)

    def stop(self):
        self.arret = 1

    def reinit(self):
        self.arret = 0
        self.compt = self.init_compt

        self.lbl.config(text='Saisissez les coordonnées:',bg="blue",fg="white",width=20)
        self.lbl.grid(column=0, row=0)
        self.txt1Lbl = Label(self.window);
        self.txt1 = Entry(self.window,width=3)
        self.txt2 = Entry(self.window,width=3)
        self.txt3 = Entry(self.window,width=3)

        self.txt1Lbl.config(text = 'X',bg="red",fg="white",width=3)
        self.txt1Lbl.grid(column=0,row=1)
        #self.lbl.pack()
        #self.txt1Lbl.pack()
        self.txt1.grid(column=1, row=1)
        self.txt2.grid(column=1, row=2)
        self.txt3.grid(column=1, row=3)

        self.NETWORK = BooleanVar()
        self.chk_state1 = BooleanVar()
        self.NETWORK.set(False)
        self.chk_state1.set(False)#set check state
        self.chk0 = Checkbutton(self.window, text='Load previous network', var=self.NETWORK)
        self.chk1 = Checkbutton(self.window, text='Learn', var=self.chk_state1)

        self.chk0.grid(column=2, row =1)
        self.chk1.grid(column=2, row =2)

        self.btn.config(text='Lancer', command=self.start)
        self.btn.grid(column=0, row=4)


I = Interface(50, 1)
