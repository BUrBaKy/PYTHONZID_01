import pdb
import os
import tkinter as tk
import ctypes

user32 = ctypes.windll.user32

from tkinter import Tk, RIGHT, BOTH, RAISED
#from tkinter.ttk import Frame, Button, Style
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from Modulele.calcule import *
from Modulele.cladire import *
from Modulele.desen import *
from Modulele.inout import *
from Modulele.structura import *

col1 = "#FFFDFA"
col2 = "#8F806F"
col3 = "#DBCFC1"
col4 = "#61818F"
col5 = "#C1D3DB"

def deschideFisier(fisier, textbox :tk.Entry):
    textbox.insert(0,"AM facut ceva...")
    fisier = filedialog.askopenfilename(initialdir = "D:\\-=Lucru=-\\Programare\\ZIDSURSA",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    textbox.delete(0, 'end')
    file_path = os.path.abspath(fisier)
    textbox.insert(0, file_path)
#    Pdb continue
    return

def deschideFereastra(master, cale1 : str, cale2 : str, ocladire : Cladire):
    objInout = Inout(cale1, cale2)
    #objInout.DeschideSiCiteste(ocladire)
    objInout.CiteseFisier(ocladire)
    #Cautam maxime pentru determinarea marimii canvas-ului
    maxWidth = maxHeight = 0
    for itEtaj in ocladire.vecEtaje:
        for itElem in itEtaj.vElem:
            count = 1
            for itDrepunghi in itElem.vecD:
                #maxWidth = max(maxWidth, itDrepunghi.origine[0]+itDrepunghi.latime)
                #maxHeight = max(maxHeight, itDrepunghi.origine[1]+itDrepunghi.inaltime) 
                maxWidth = max(maxWidth, itDrepunghi.d1+itDrepunghi.b)
                maxHeight = max(maxHeight, itDrepunghi.d2+itDrepunghi.h) 

    fereastra = tk.Toplevel(master)
    desenfereastra = desenWindow(fereastra, maxWidth, maxHeight)
    ratieX = user32.GetSystemMetrics(0) / maxWidth
    ratieY = user32.GetSystemMetrics(1) / maxHeight
    ratie = min(ratieX, ratieY)
    iEtajCounter = 0
    for itEtaj in ocladire.vecEtaje:
        iEtajCounter+=1
        iElemCounter = 0
        for itElem in itEtaj.vElem:
            iElemCounter +=1
            iDreptunghiCounter = 0
            for itDrepunghi in itElem.vecD:
                iDreptunghiCounter += 1
                nume = itElem.nume + str(count)
                iID = int(iEtajCounter * 1e6 + iElemCounter * 1e3 + iDreptunghiCounter)
                #desenfereastra.Add_Rectangle(iID, nume, itDrepunghi.origine[0]*ratie, itDrepunghi.origine[1]*ratie, itDrepunghi.latime*ratie, itDrepunghi.inaltime*ratie)        
                desenfereastra.Add_Rectangle(iID, nume, itDrepunghi.d1*ratie, itDrepunghi.d2*ratie, itDrepunghi.b*ratie, itDrepunghi.h*ratie)        

    yesNoDialog = messagebox.askyesno('Motor Calcul', 'Doriti sa facem calculul?')
    if yesNoDialog == True:
        mtrCalc = MotorCalcul()      
        try:
            mtrCalc.Calculeaza(ocladire)    
        except:
            messagebox.showinfo('Eroare la calcul!', 'Eroare la calcul!')

    yesNoDialog = messagebox.askyesno('Fisier InOut', 'Doriti sa facem salvarea pe disc?')
    if yesNoDialog == True:
        objInout.SalvareDate(ocladire)
        
    #elemCurent = ocladire.vecEtaje[0].vElem[0]
    #desenfereastra.Add_Rectangle("Id1",elemCurent.origine[0], elemCurent.origine[1], elemCurent.latime, elemCurent.inaltime)

window = tk.Tk()

window.title("Aleluia")
#window.geometry("800x600")
window.configure(bg=col3)

Frame_Top = tk.Frame(window, relief="solid", bg=col3, height=36,  borderwidth=1)

#FRAME_MID_1
Frame_Mid_1 = tk.Frame(window, relief="solid", bg=col3, height=200, borderwidth=1, pady=20)

fisier1 = 0
but1 = tk.Button(Frame_Mid_1, text = "Seteaza fisier intrare", font=("Helvetica", 12))
but2 = tk.Button(Frame_Mid_1, text = "Seteaza fisier rezultate", font=("Helvetica", 12))

#FRAME_MID_2
Frame_Mid_2 = tk.Frame(window, relief="solid", bg=col3, height=200, borderwidth=1, pady=20)

cale1 = tk.Entry(Frame_Mid_2, width=60)
cale2 = tk.Entry(Frame_Mid_2, width=60)

but1.configure(command = lambda:deschideFisier(fisier1, cale1))
but2.configure(command = lambda:deschideFisier(fisier1, cale2))
#FRAME_BOT
ocladire = Cladire()
Frame_Bot = tk.Frame(window, pady=30, bg=col3)
but3 = tk.Button(Frame_Bot, text = "Ruleaza program", font=("Helvetica", 12), padx=3, pady=3)
but3.configure(command = lambda:deschideFereastra(window, cale1.get(), cale2.get(), ocladire))

######PACKING THE STUFF############

Frame_Top.pack(fill = "both", side="top")
tk.Label(master=Frame_Top, text="Program calcul zidarie", fg = col4, bg=col3, font=("Helvetica", 16)).pack()
Frame_Mid_1.pack(fill = "y")
but1.pack(side="left")
tk.Label(Frame_Mid_1, bg=col3, width=30).pack(side="left")
but2.pack(side="left")

Frame_Mid_2.pack(fill = "y")

tk.LabelFrame(Frame_Mid_2, width=15).pack(side="left")
tk.Label(Frame_Mid_2, text="Cale:", padx=10).pack(side="left")
tk.LabelFrame(Frame_Mid_2, width=15).pack(side="left")

cale1.pack(side="left")
tk.Label(Frame_Mid_2, bg=col3, width=30).pack(side="left")
cale2.pack(side="left")
tk.LabelFrame(Frame_Mid_2, width=15).pack(side="left")
tk.Label(Frame_Mid_2, text="Cale:", padx=10).pack(side="left")
tk.LabelFrame(Frame_Mid_2, width=15).pack(side="left")

Frame_Bot.pack()
but3.pack()

window.mainloop()

#Added simple comment just for testing version control


      