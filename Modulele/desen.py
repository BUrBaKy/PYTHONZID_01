import tkinter as tk
from tkinter import messagebox
#from .. import structura
from .structura import *

class desenWindow:
    forme = {}
    def __init__(self, master, maxWidth, maxHeight):
        self.master = master
        master.title("A simple GUI")

        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.m_Canvas = tk.Canvas(master, width=maxWidth, height=maxHeight, bg="white", borderwidth=5, relief="ridge")
        self.m_Canvas.pack()
    
    def Add_RectangleInitial(self, nume):
        #messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
        drpt = Dreptunghi((125 ,135) , 100, 100)
        #messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
        #self.forme[nume] = self.m_Canvas.create_rectangle(drpt.x, drpt.Dx, drpt.x, drpt.Dy)
        #self.m_Canvas.create_rectangle(25, 25, 100, 100, fill="red") merge!
        self.forme = {"d1" : self.m_Canvas.create_rectangle(25, 25, 100, 100, fill="red") }
        self.forme = {"d1" : self.m_Canvas.create_rectangle(25, 25, 60, 60, fill="green") }
        #self.forme[nume] = self.m_Canvas.create_rectangle(drpt.origine[0], drpt.origine[1], drpt.origine[0]+drpt.latime, drpt.origine[1]+drpt.inaltime, fill="blue")
        self.forme[nume] = self.m_Canvas.create_rectangle(drpt.d1, drpt.d2, drpt.d1 + drpt.b, drpt.d2 + drpt.h, fill="blue")
        messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
        self.m_Canvas.delete(self.forme[nume])

    def Add_Rectangle(self, iID, strNume, centruX, centruY, dimX, dimY):       
        obiect = self.m_Canvas.create_rectangle(int(centruX-dimX/2), int(centruY-dimY/2), int(centruX+dimX/2), int(centruY+dimY/2), fill="blue")
        self.forme[iID] = obiect

            
   


