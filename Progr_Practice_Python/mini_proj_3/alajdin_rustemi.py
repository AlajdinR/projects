from Tkinter import *
import clusters
import tkFont
import ttk
import tkFileDialog
import tkMessageBox
from os import *
import anydbm
from math import sqrt
import pickle
from PIL import Image, ImageDraw
import re
import feedparser


class Proj3(Frame): #Here I'm creating the main Class with Frame in it
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        self.parent = parent
        self.parent.title('Course Analyzer-Sehir limited edition ') #Just putting the title of the frame/we could do it bellow aswell
        ttk.Style().configure("TFrame", background="#F333")
        self.interface(parent) #We are calling the i,nterface function,which takes care of all the interface we need
        self.pack(fill = BOTH, expand = 1)



    #Bellow we defined the Interface function, here we have created all the needed Frames, Buttons, Labels , Radiobuttons, ListBoxes, and the Canvas, and we have made a combination of
    #both grid and pack geometry manager to fit them on the main Frame according to our wish. However, we have never used both .grid and .pack together
    def interface(self,parent):
        Label(text = 'COURSE ANALYZER - SEHIR LIMITED EDITION',  bg = "red", fg = "white",font = ("Helvetica", 14),anchor = CENTER).pack(fill = X, expand = 0)
        self.frame1 = Frame(parent)
        self.frame1.pack(fill = X, expand = True)
        Label(self.frame1, text = 'Upload a file that contains course descriptions:', anchor = NW).pack(side = LEFT, fill = X , expand = 0)
        Button(self.frame1, text = 'Browse',command = self.browse_button, anchor = CENTER, width = 7, font = ('Helvetica', 9,'bold') ).pack(side = LEFT, expand = 0, fill = X, padx = 55)
        self.frame2 = Frame(parent)
        self.frame2.pack(fill = X, expand = 1)
        Label(self.frame2, text = 'Selected File: ', anchor = NW ).pack(side = LEFT, fill = X, expand = 0)
        self.getpath = StringVar() #I will need to use this latter
        self.getpath.set('Please select a file')
        self.path_label = Label(self.frame2,textvariable = self.getpath, anchor = CENTER,borderwidth = 3, relief = SOLID)
        self.path_label.pack(side = TOP, fill = X, expand = 0)
        self.frame3 = Frame(parent, bd = 3, relief = SOLID,height = 900)
        self.frame3.columnconfigure(0, weight = 1)
        self.frame3.rowconfigure(0, weight = 1)
        self.frame3.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)
        self.frame3_1 = Frame(self.frame3)
        self.frame3_1.grid(sticky = W+E,row = 0, column = 0)
        Label(self.frame3_1,text = 'Similarity Measure: ', anchor = CENTER, font =('Times',12,'italic')).pack(side = RIGHT, fill = X, expand = 1)
        self.frame3_2 = Frame(self.frame3)
        self.frame3_2.grid(sticky = W+E, row = 0, column = 1)
        self.radio_select = StringVar() #I will need to use this one aswell
        Radiobutton(self.frame3_2, text="Pearson", variable=self.radio_select, value='pearson').pack(anchor=W,padx = 25, expand = 0)
        Radiobutton(self.frame3_2, text="Tanimoto", variable=self.radio_select, value='tanimoto').pack(anchor=W, padx = 25,pady = 5, expand = 0)
        self.radio_select.set('pearson')
        self.frame3_3 = Frame(self.frame3)
        self.frame3_3.grid(sticky =W+E, row = 0, column = 2)
        Label(self.frame3_3, text = 'Select Course Codes: ',font = ('Helvetica',10,'bold'), anchor = NE).pack(side = LEFT, fill = BOTH, expand = 1, pady = 5)
        self.frame3_x = Frame(self.frame3)
        self.frame3_x.grid(sticky = W+E, row =0, column = 3)
        self.scrollbar = Scrollbar(self.frame3_x, orient=VERTICAL)
        self.choices = StringVar
        #self.choices.set(None)
        self.listbox = Listbox(self.frame3_x, yscrollcommand=self.scrollbar.set, selectmode = MULTIPLE,height = 5 )
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame3_4 = Frame(self.frame3)
        self.frame3_4.grid(row = 1,column = 0, columnspan = 3,pady = 5)
        #Should make command functions for bellow 3 buttons
        Button(self.frame3_4, text = 'Draw Hierarchical Cluster Diagram',command = self.draw_dendo_Button1, anchor = CENTER, font = ('Helvetica', 9,'bold')).pack(side = LEFT, expand = 0, fill = X, padx = 10)
        Button(self.frame3_4, text = 'Print Hierarchical Cluster as Text',command = self.printData_Button2,  anchor = CENTER, font = ('Helvetica', 9,'bold')).pack(side = LEFT, expand = 0, fill = X, padx = 10)
        Button(self.frame3_4, text = 'Show Data Matrix',command = self.printMatrix_Button3,  anchor = CENTER, font = ('Helvetica', 9,'bold')).pack(side = LEFT, expand = 0, fill = X, padx = 10)
        self.frame3_5 = Frame(self.frame3,height = 700)
        self.frame3_5.columnconfigure(0, weight = 1)
        self.frame3_5.rowconfigure(0, weight = 1)
        self.frame3_5.grid(row = 2, column = 0, columnspan = 4,rowspan = 4,  sticky = N+E+S+W)
        self.canvas=Canvas(self.frame3_5,bg='#FFFFFF',width=300,height=700, scrollregion = (0,0,self.winfo_screenwidth()+10000,self.winfo_screenheight()+2500))
        
        self.vertical_scroll = Scrollbar(self.frame3_5,orient=VERTICAL)
        self.vertical_scroll.grid(row = 0, column = 1, sticky = N+S)   #pack(side=RIGHT,fill=Y)
        self.vertical_scroll.config(command = self.canvas.yview)
        self.horizontal_scroll = Scrollbar(self.frame3_5,orient=HORIZONTAL)
        self.horizontal_scroll.grid(row = 1, column = 0, sticky = W+E)    #pack(side=BOTTOM,fill=X)
        self.horizontal_scroll.config(command = self.canvas.xview)
        self.canvas.config(xscrollcommand = self.horizontal_scroll.set,yscrollcommand = self.vertical_scroll.set)
        self.canvas.config(width = 300, height = 300)
        self.canvas.grid(row = 0, column = 0, sticky = N+E+S+W)
        





#This function represents the command of the 'Browse' button, when we press on 'Browse' button, this function is executed, letting us to choose a file from the dialogefile
    #This function also automatically populates the listbox with the needed course codes as required in the project sheet. However, it does that by calling another function we have
    #defined bellow
    def browse_button(self):
        self.file_path = tkFileDialog.askopenfile()
        self.getpath.set(self.file_path.name)
        self.populate_listbox(self.file_path.name)
        self.canvas.delete("all")
        return self.file_path.name




    #This is the function that gets called when we want to populate the ListBox.
    #We firstly open the file by the create_file function which we have defined bellow, then we use some string methods to get the Course Codes only and only once,
    #Afterwards we put all those  Unique Course Codes in a list , and then we insert the elements of the list in the ListBox
    def populate_listbox(self,loc):
        self.filetoread=  self.create_file(str(loc))
        self.showList = []
        for string in self.lines:
            if string.split()[0] not in self.showList:
                self.showList.append(string.split()[0])
        self.listbox.delete(0, END)
        for key in self.showList:
            self.listbox.insert(END,key)
        return self.showList



    #We have defined this function just so that we keep track of what choices we have made on the ListBox. We put our choices as strings in a list called rlist.
    def selectt(self):
        self.rlist = []
        self.sel = self.listbox.curselection()
        for i in self.sel:
            self.rlist.append(self.listbox.get(i))
        return self.rlist




    #Here, we want to make a function which will return something similar to what the clusters.readfile() returns, but with small changes
    #We want to have only the courses related to what Course Codes we have selected from the ListBox, and also only the words that are used under the course
    #related to those Course Codes we have selected. Afterwards, we want the word counts of only those words that we mentioned above, not all the words in the file.
    #If we look at the function, thats actually what we do: We go through the items of what we selected from ListBox, then for each item we check where this item is in
    #self.lines(its a list returned from create_file function which holds all the course names and codes). Afterwards, we get all the items related to what we have selected,
    #and in the meanwhile we get all the words of the courses related to what we have selected from the ListBox in another List, and lastly we get the wordcounts of these words
    #in a third list
    def before_Clustering(self):
        self.selectt()
        self.rownamess = []
        self.columnnamess = []
        self.data = []
        print self.rlist
        for item in self.rlist:
            for itt in self.lines:
                if itt.startswith(item):
                    self.rownamess.append(itt)
                    for elem in self.otherlines[self.lines.index(itt)]:
                        if elem not in self.columnnamess:
                            self.columnnamess.append(elem)
                        else: pass
                else: pass
        for itemm in self.rownamess:
            self.data.append([float(self.otherlines[self.lines.index(itemm)].count(element)) for element in self.columnnamess])
        return self.rownamess, self.columnnamess, self.data





    #This function is very similar to the one we have in clusters.py. We have mane few changes however. This one is drawing in canvas instead of creating an image.
    #And also it calculates the distances between the nodes when we draw on canvas. This function is iterative, and is part of another function defined bellow
    def drawnode(self, clust, x, y, scaling, labels):
        if clust.id < 0:
            self.h1 = clusters.getheight(clust.left) * 20
            self.h2 = clusters.getheight(clust.right) * 20
            #self.h1 and self.h2 doesn't allways give needed values.In other words getheight() and getdepth() don't allways work as we want. I couldn't fix this one
            self.top = x - (self.h1 + self.h2)
            self.bottom = x + (self.h1 + self.h2)
            self.ll = clust.distance * scaling/2
            self.canvas.create_line(self.top + self.h1/2,y , self.bottom - self.h2/2,y )

            self.canvas.create_line(self.top + self.h1/2 ,y ,self.top + self.h1/2 , y + self.ll)

            self.canvas.create_line(self.bottom - self.h2/2, y, self.bottom - self.h2 /2, y + self.ll)
            self.drawnode(clust.left, self.top + (self.h1/2), y+self.ll , scaling, labels )
            self.drawnode(clust.right, self.bottom - (self.h2/2), float(y+self.ll) , scaling, labels )
        else:
            self.cc =self.canvas.create_text(x-5, y+7)
            self.canvas.itemconfig(self.cc, text = labels[clust.id])




    #This is the function that actually draws the clustering on canvas. Basically, it only makes the first starting line and calculates the coordinates, and after that,
    #it calls the drawnode function which we have defined and explaied above. We have been insired by the Drawdendogram function defined in clusters.py to make this function.
    #And the drawing is actually working perfect. But as I said, the getheight() function does not allways work in our favor, which also makes the drawing not allways look good.
    def mYdendogram(self, clust, labels):
        self.h = clusters.getheight(clust) * 20
        self.w = 1200
        self.depth = clusters.getdepth(clust)
        self.scaling = float(self.w - 150) / self.depth

        self.canvas.create_line(self.h*4, 0 , self.h*4,10)
        self.drawnode(self.clust, (self.h*4),10 , self.scaling, labels)



    #This is the function which is called when we press the 'Draw Hierarchical Cluster Diagram' button. It calls multiple functions inside(both our and clusters.py functions)
    #We have mentioned already what the called functions inside do, and also we have already mentioned the source of th issue arised here(getheight() or clust.right)
    def draw_dendo_Button1(self):
        self.rownamess, self.columnnamess,self.data = self.before_Clustering()
        print self.radio_select.get()
        if self.radio_select.get() == 'pearson':
            self.clust = clusters.hcluster(self.data,distance=clusters.pearson)
        else:
            self.clust = clusters.hcluster(self.data,distance=clusters.tanimoto)
        self.canvas.delete("all")
        self.mYdendogram(self.clust, self.rownamess)






    #This is the function called when the 'Print Hierarchical Cluster as Text' button is pressed. We just want to make a string representation of the clustering and the
    #clusters.clust2str function does that for us. All we have to do is play wth the code so that we write all this inside canvas
    def printData_Button2(self):
        self.rownamess, self.columnnamess,self.data = self.before_Clustering()
        if self.radio_select.get() == 'pearson':
            self.clust = clusters.hcluster(self.data,distance=clusters.pearson)
        else:
            self.clust = clusters.hcluster(self.data,distance=clusters.tanimoto)
        self.canvas.delete("all")
        self.canvas_id =self.canvas.create_text(150,10, anchor = NW)
        self.canvas.itemconfig(self.canvas_id, text = clusters.clust2str(self.clust, self.rownamess))



    # This is the function which gets caled when the 'Show Data Matrix' button gets pressed. Its a function defined by us. We play with the data we get from the before_Clustering function
    # and by for loops and if statements,  we for one single string that has the form that we want(the matrix form). After we do this , we put this string inside the canvas
    def printMatrix_Button3(self):
        self.rownamess, self.columnnamess,self.data = self.before_Clustering()
        self.canvas.delete("all")
        self.canvas_id2 = self.canvas.create_text(0,0, anchor = NW)
        self.str = (len(max(self.rownamess))+1)* '  ' #Just some spaces on the Top-Left corner so that it doesn't look too confusing
        for item in self.columnnamess:
            self.str += item + '\t'
        self.str += '\n'
        for i in range(len(self.rownamess)):
            self.str += self.rownamess[i] + '\t'
            for j in range(len(self.columnnamess)):
                self.str += str(self.data[i][j]) + '\t'
            self.str += '\n'
        self.str += '\n'
        self.canvas.itemconfig(self.canvas_id2, text = self.str )

    # This function gets called severall times. what it does is it opend the file we want to work with, then it creates a list of all the course names, another list which contains
    #lists of the words used for each and every course, and lastly it creates a list containing all the possible words used in the file once only
    def create_file(self, filename):
        self.lines = []
        self.otherlines = []
        self.allwords = []
        for i,item in enumerate(file(filename)):
            if i%2 ==0:
                a = item.split()
                self.lines.append('%s %s'%(a[0], a[1]))
            else:
                self.otherlines.append(clusters.getwords(item))
        for list1 in self.otherlines:
            for word in list1:
                if word not in self.allwords:
                    self.allwords.append(word)
        return self.lines, self.otherlines,self.allwords








def main():



    root = Tk()
    app = Proj3(root)
    app.winfo_geometry()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()

main()
