
"""
 Alajdin Rustemi
 St.Number: 213142080
"""
from xlrd import open_workbook
from selenium import webdriver
import ttk
import tkFileDialog
from Tkinter import *  # Python 2
from PIL import ImageTk, Image
import os
from tkColorChooser import askcolor
from tkMessageBox import showerror, showwarning  # Python 2
from bs4 import BeautifulSoup,NavigableString, Tag
import urllib2
import re
import time
import ScrolledText
import sys
reload(sys)
sys.setdefaultencoding('utf8')








class MyPaint(Frame):
    def __init__(self, master):
        """
        Initializing all the parts of the GUI,
            defining all of our main variables...
        :param master:
        :return:
        """

        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #Photos/asserts
        self.rectPhoto = ImageTk.PhotoImage(Image.open("rectangle.png"))
        self.ovalPhoto = ImageTk.PhotoImage(Image.open("oval.png"))
        self.eraserPhoto = ImageTk.PhotoImage(Image.open("eraser.png"))
        self.linePhoto = ImageTk.PhotoImage(Image.open("line.png"))
        self.dragPhoto = ImageTk.PhotoImage(Image.open("drag.png"))
        self.buttPhoto = ImageTk.PhotoImage(Image.open("beautify.png"))

        #Variables
        self.drawRect = True
        self.drawOval = False
        self.drawLine = False
        self.drag = False
        self.erase = False
        self.fillColor = (0, "dark green")  #Default fill color
        self.borderColor =(0,"red")   #Default border color
        self.mainD = dict()
        self.rearrange = False




        #Frames
        self.upper_frame = Frame()
        self.middle_frame = Frame()
        self.lower_frame = Frame()
        self.ins_mid_F = Frame(self.middle_frame)


        # Labels
        self.titleLabel = Label(self.upper_frame, text = "My Paint", fg = "white", bg = "dark orange", font=('Helvetica', 19), height=2)
        self.rectLabel = Label(self.ins_mid_F,image = self.rectPhoto )
        self.ovalLabel = Label(self.ins_mid_F,image = self.ovalPhoto )
        self.eraserLabel = Label(self.ins_mid_F,image = self.eraserPhoto )
        self.lineLabel = Label(self.ins_mid_F,image = self.linePhoto )
        self.dragLabel = Label(self.ins_mid_F,image = self.dragPhoto )
        self.fill = Label(self.ins_mid_F, text = "Fill Color: ")
        self.fillcolorL = Label(self.ins_mid_F,width = 4, bg = self.fillColor[1])  #will come latter here
        self.border = Label(self.ins_mid_F, text = "Border Color: ")
        self.bordercolorL = Label(self.ins_mid_F, width = 4,bg = self.borderColor[1])
        self.weightL = Label(self.ins_mid_F, text = "Weight: ")
        self.spinn = Spinbox(self.ins_mid_F, from_ = 1, to = 100,width = 7)
        self.canvas = Canvas(self.lower_frame, bg ="white",cursor = "cross" )


        #Buttons
        self.beautyB = Button(self.ins_mid_F,image = self.buttPhoto, width = 50, height = 19, command = self.beautyfy)




        self.interface()
        self.rectLabel.config(relief = SUNKEN)


        self.rectLabel.bind('<Button-1>', self.rect_label_press)
        self.ovalLabel.bind('<Button-1>', self.oval_label_press)
        self.eraserLabel.bind('<Button-1>', self.erase_label_press)
        self.lineLabel.bind('<Button-1>', self.line_label_press)
        self.dragLabel.bind('<Button-1>', self.drag_label_press)
        self.canvas.bind('<ButtonPress-1>', self.canvasSelect)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)
        self.bordercolorL.bind('<Button-1>', self.getBorderColor)
        self.fillcolorL.bind('<Button-1>', self.getFillColor)




    def interface(self):
        self.upper_frame.pack(fill = X, expand = 0,side = TOP)
        self.middle_frame.pack(fill = X, expand = 0)
        self.lower_frame.pack(fill = BOTH, expand = 1)
        self.ins_mid_F.pack(fill = X, expand = 1, side = TOP,padx = 310)

        #Variables
        self.dist = (self.root.winfo_width() - self.ins_mid_F.winfo_width())/2

        self.beautyB.pack(fill = X, expand = 0, side = LEFT,padx = 10)


        #Labels
        self.titleLabel.pack(fill = X, expand = 0,side = TOP )
        self.rectLabel.pack(side = LEFT, fill = X, expand = 0)
        self.ovalLabel.pack(side = LEFT, fill = X, expand = 0)
        self.lineLabel.pack(side = LEFT, fill = X, expand = 0)
        self.dragLabel.pack(side = LEFT, fill = X, expand = 0)
        self.eraserLabel.pack(side = LEFT, fill = X, expand = 0)
        self.fill.pack(side = LEFT, fill = X, expand = 0)
        self.fillcolorL.pack(side = LEFT, fill = X, expand = 0)
        self.border.pack(side = LEFT, fill = X, expand = 0)
        self.bordercolorL.pack(side = LEFT, fill = X, expand = 0)
        self.weightL.pack(side = LEFT, fill = X, expand = 0)
        self.spinn.pack(side = LEFT, fill = X, expand = 0)
        self.canvas.pack(fill = BOTH,expand = 1,padx = 20, pady = 10)




    def beautyfy(self):
        for itemm in self.canvas.find_all():
            checkCords = self.canvas.coords(itemm)
            if len(self.canvas.find_overlapping(checkCords[0],checkCords[1],checkCords[2],checkCords[3])) != 1:
                self.rearrange = True
                break
        if self.rearrange:
            self.initX = 0
            self.initY = 0
            for item in self.canvas.find_all():
                coords = self.canvas.coords(item)
                #if self.initX+(coords[2]-coords[0])>self.canvas.winfo_width()
                self.canvas.coords(item, self.initX,self.initY,self.initX +(coords[2]-coords[0]),self.initY +(coords[3]-coords[1]) )
                self.initX = self.initX +(coords[2]-coords[0]) + 1
                #self.initY = self.initY +(coords[3]-coords[1])
            self.rearrange = False



    def getBorderColor(self,event):
        prev = self.borderColor
        self.borderColor = askcolor(title = "My Colour Chooser", initialcolor= "red")
        if self.borderColor[1] == None:
            self.borderColor = prev
        self.bordercolorL.config(bg =self.borderColor[1])


    def getFillColor(self,event):
        prev = self.fillColor
        self.fillColor = askcolor(title = "My Colour Chooser", initialcolor= "dark green")
        if self.fillColor[1] == None:
            self.fillColor = prev
        self.fillcolorL.config(bg =self.fillColor[1])

    def make_all_normal(self):
        self.rectLabel.config(relief = FLAT)
        self.ovalLabel.config(relief = FLAT)
        self.eraserLabel.config(relief = FLAT)
        self.lineLabel.config(relief = FLAT)
        self.dragLabel.config(relief = FLAT)
        self.border.config(state = NORMAL)
        self.bordercolorL.config(state = NORMAL)
        self.drawRect = False
        self.drawOval = False
        self.drawLine = False
        self.drag = False
        self.erase = False



    def rect_label_press(self,event):
        self.make_all_normal()
        self.rectLabel.config(relief = SUNKEN)
        self.drawRect = True

    def oval_label_press(self,event):
        self.make_all_normal()
        self.ovalLabel.config(relief = SUNKEN)
        self.drawOval = True

    def erase_label_press(self,event):
        self.make_all_normal()
        self.eraserLabel.config(relief = SUNKEN)
        self.erase = True

    def line_label_press(self,event):
        self.make_all_normal()
        self.lineLabel.config(relief = SUNKEN)
        self.border.config(state = DISABLED)
        self.bordercolorL.config(state = DISABLED)
        self.drawLine = True

    def drag_label_press(self,event):
        self.make_all_normal()
        self.dragLabel.config(relief = SUNKEN)
        self.drag = True



    def canvasSelect(self, event):
        if self.drag or self.erase:
            return
        else:
            self.startx, self.starty = event.x, event.y
            if self.drawOval:
                item = self.canvas.create_oval(self.startx, self.starty, event.x, event.y, outline=self.borderColor[1],width = float(self.spinn.get()))
            elif self.drawRect:
                item = self.canvas.create_rectangle(self.startx, self.starty, event.x, event.y, outline=self.borderColor[1],width = float(self.spinn.get()))
            elif self.drawLine:
                item = self.canvas.create_line(self.startx, self.starty, event.x, event.y,width = float(self.spinn.get()))

            self.canvas.tag_bind(item, '<ButtonPress-1>', self.itemSelect)
            self.canvas.tag_bind(item, '<B1-Motion>', self.itemDrag)
            self.canvas.tag_bind(item, '<ButtonRelease-1>', self.itemDrop)

            self.drawnItem = item

    def canvasDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        if self.drawOval or self.drawLine or self.drawRect:
            item = self.canvas.find_closest(event.x, event.y)
            self.canvas.coords(self.drawnItem, self.startx, self.starty, event.x, event.y)


    # Added for Part 4
    def canvasDrop(self, event):
        """Drops this item."""
        if self.drawOval or self.drawLine or self.drawRect:
            self.canvas.itemconfig(self.drawnItem, fill=self.fillColor[1]) # change color
            self.mainD[self.drawnItem] = self.canvas.coords(self.drawnItem)


    def itemSelect(self, event):
        """Selects this item for dragging."""
        if self.erase:
            self.eraseitem =  self.canvas.find_closest(event.x, event.y)
            self.canvas.delete(self.eraseitem)
            if self.eraseitem[0] in self.mainD.keys(): del self.mainD[self.eraseitem[0]]

            return
        elif self.drag:
            self.dragx, self.dragy = event.x, event.y
            self.dragitem = self.canvas.find_closest(event.x, event.y)



    # Added for Part 3:
    def itemDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        if not self.drag:
            return
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y


    # Added for Part 3:
    def itemDrop(self, event):
        """Drops this item."""
        if not self.drag:
            return
        self.mainD[self.dragitem[0]] = self.canvas.coords(self.drawnItem)











if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    #root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('MyPaint')  # Set GUI Title
    root.minsize('900', '700')
    root.geometry('{}x{}+250+0'.format('1100', '850'))  # Set GUI geometry
    app = MyPaint(root)  # Starting our app and passing tables to our app.
    root.mainloop()  # Show GUI to user