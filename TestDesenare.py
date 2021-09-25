import win32api
import tkinter as tk
from tkinter import Event, messagebox
from tkinter.constants import FALSE


class desenTest:
    forme = []
    x = 0
    y = 0
    iSign = 0
    arrSigns = [[1,1], [1, -1], [-1,-1], [-1,1]]
    bShowRectang = True
    redRectang = 0
    magnetPower = 40
    magnetRectang = 0
    magnetFill = ""
    magnetAlpha = 0.3
    def addRectangleToList(self, width, height, color):
        self.forme.append (self.m_Canvas.create_rectangle(self.x, self.y, self.otherX(width), self.otherY(height), fill=color))

    def otherX(self, dim):
        sign = self.arrSigns[self.iSign][0]
        return self.x + sign*dim

    def otherY(self, dim):
        sign = self.arrSigns[self.iSign][1]
        return self.y + sign*dim

    def isInsideRectang(self, P1, rectang):
        if  rectang[0] < P1[0] and P1[0] < rectang[2] and rectang[1] < P1[1] and P1[1] < rectang[3]: 
            return True
        else:
            return False
    
    def snapToNearby(self, magnetCoords):
        if magnetCoords == 0:
            return

        bIsInside = False
        p = (0,0)
        for forma in self.forme:
            formaCoords = self.m_Canvas.coords(forma)
            #magnetCoords = self.m_Canvas.coords(prevMagnet)
            p = (formaCoords[0], formaCoords[1])
            if self.isInsideRectang(p, magnetCoords):
                print("P1!!!")
                bIsInside = True
                break
            p = (formaCoords[2], formaCoords[1])
            if self.isInsideRectang(p, magnetCoords):
                print("P2!!!")
                bIsInside = True
                break
            p = (formaCoords[2], formaCoords[3])
            if self.isInsideRectang(p, magnetCoords):
                print("P3!!!")
                bIsInside = True
                break
            p = (formaCoords[0], formaCoords[3])
            if self.isInsideRectang(p, magnetCoords):
                print("P4!!!")
                bIsInside = True
                break
            
        if bIsInside == True:
            self.magnetFill = "Green"
        return p

    def reset(self):
        self.m_Canvas.delete(self.redRectang)
        prevMagnetCoords = self.m_Canvas.coords(self.magnetRectang)
        self.m_Canvas.delete(self.magnetRectang)
        self.magnetFill = ""
        return prevMagnetCoords

    def motion(self, event):        
        prevMagnetCoords = self.reset()
        self.x, self.y = event.x, event.y     
        print('{}, {}'.format(self.x, self.y))   
        if (self.bShowRectang):
            self.redRectang = self.m_Canvas.create_rectangle(self.x, self.y, self.otherX(100), self.otherY(100), fill="red")
        self.snapToNearby(prevMagnetCoords)
        self.magnetRectang = self.m_Canvas.create_rectangle(self.x - self.magnetPower / 2, self.y - self.magnetPower / 2, 
                                  self.x + self.magnetPower / 2, self.y + self.magnetPower / 2, fill = self.magnetFill )  
                                  #self.magnetFill, alpha = self.magnetAlpha

    def click1(self, event):
        crtMagnetCoords = self.m_Canvas.coords(self.magnetRectang)
        p = self.snapToNearby(crtMagnetCoords)
        if (p!=(0,0)):
            self.x = p[0]
            self.y = p[1]

        self.addRectangleToList(100, 100, 'blue')

    def tabKey(self, event):
        if (self.iSign < 3):
            self.iSign += 1
        else :
            self.iSign = 0
        print("Tab was pressed at {},{}", self.x, self.y)

    def showItems(self, event):
        counter = 1
        for forma in self.forme:
            coords = self.m_Canvas.coords(forma)
            print("Dreptunghiul nr. %d :  [%d,%d - %d,%d] " % (counter, coords[0],  coords[1],  coords[2],  coords[3]))
            counter += 1
    
    def modifyMagnetPower(self, event):
        self.magnetPower += (event.delta / 50)

    def __init__(self, master, maxWidth, maxHeight):
        self.master = master
        master.title("A simple GUI")

        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.m_Canvas = tk.Canvas(master, width=maxWidth, height=maxHeight, bg="white", borderwidth=5, relief="ridge")
        self.m_Canvas.create_line(0,0,100,100)
        self.m_Canvas.pack()
        master.bind('<Motion>', 
                    lambda event : 
                        self.motion(event))
        master.bind("<Button-1>", lambda event : self.click1(event))
        master.bind("<Tab>", lambda event: self.tabKey(event))
        master.bind("<Button-3>", lambda event : self.showItems(event))
        master.bind("<MouseWheel>", lambda event : self.modifyMagnetPower(event))
#    def motion(event):
#        x, y = event.x, event.y
#        print('{}, {}'.format(x, y)) 
 
"""
#    def Add_RectangleInitial(self, nume):
#        #messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
#        drpt = structura.dreptunghi((125 ,135) , 100, 100)
#        #messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
#        #self.forme[nume] = self.m_Canvas.create_rectangle(drpt.x, drpt.Dx, drpt.x, drpt.Dy)
#        #self.m_Canvas.create_rectangle(25, 25, 100, 100, fill="red") merge!
#        self.forme = {"d1" : self.m_Canvas.create_rectangle(25, 25, 100, 100, fill="red") }
#        self.forme = {"d1" : self.m_Canvas.create_rectangle(25, 25, 60, 60, fill="green") }
#        self.forme[nume] = self.m_Canvas.create_rectangle(drpt.origine[0], drpt.origine[1], drpt.origine[0]+drpt.latime, drpt.origine[1]+drpt.inaltime, fill="blue")
#        messagebox.showinfo("deschideFereastra", "a Tk MessageBox")
#        self.m_Canvas.delete(self.forme[nume])

#    def Add_Rectangle(self, iID, strNume, centruX, centruY, dimX, dimY):       
#        obiect = self.m_Canvas.create_rectangle(int(centruX-dimX/2), int(centruY-dimY/2), int(centruX+dimX/2), int(centruY+dimY/2), fill="blue")
#        self.forme[iID] = obiect
"""

#End of header

window = tk.Tk()
dt = desenTest(window, 800, 600)
#window.bind('<Motion>', desenTest.motion)
window.mainloop()