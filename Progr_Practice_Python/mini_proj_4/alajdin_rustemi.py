from tkinter import *
from PIL import Image, ImageTk
from ttk import Combobox
import tkFileDialog, tkMessageBox, os, xlrd, pickle, anydbm
from math import sqrt
import ttk
import urllib2
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import io



class Proj4(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        self.parent = parent
        self.parent.title('SEHIR Reserh Projects Analyzer ')
        ttk.Style().configure("TFrame", background="#F333")
        self.interface(parent)
        self.pack()



    def interface(self,parent):
        Label(text = 'SEHIR Research Projects Analyzer -CS Edition',width = 50,  bg = "Blue", fg = "white",font = ("Helvetica", 14, 'bold'),anchor = CENTER).pack(fill = None, expand = 0)
        self.frame0 = Frame(self.parent)
        self.frame0.pack(fill = BOTH, expand = True,side = TOP)
        self.frame1 = Frame(self.frame0)
        self.frame1.pack(fill = X, expand = 0, side = LEFT)
        self.url = Label(self.frame1,text ='Please Provide a url:',font = ("Helvetica", 9, 'bold'), anchor = W).grid(column = 0, row = 0, padx = 7, sticky = W+N)
        self.webpage = StringVar  #We might use the strinvar so that we get the info we provide in the entry
        self.urlEntry = Entry(self.frame1,bg = 'yellow', width = 50,textvariable = self.webpage)
        self.urlEntry.grid(column = 0, row = 1,columnspan = 3, padx = 7, pady = 10, sticky = W+E)
        self.frame2 = Frame(self.frame0)
        self.frame2.pack(fill = X, expand = 0, side = LEFT)
        Button(self.frame2, text = 'Fetch Reserch Projects',command = self.fetchButton, anchor = CENTER,font = ("Helvetica", 9, 'bold'), width = 30).pack(side = LEFT, fill = X, expand = 0, padx = 20)
        Label(text = '"'* (self.frame1.winfo_screenwidth()/7)).pack(fill = X, expand = 1)
        self.frame3 = Frame(self.parent)
        self.frame3.pack(fill = X, expand = 1, side = TOP)
        Label(self.frame3 , text = 'Filter Reserch Projects By:',font = ("Helvetica", 12, 'bold'),anchor = W).grid(column = 0, row = 0)
        Label(self.frame3 , text = 'Pick a Project:',font = ("Helvetica", 12, 'bold'), anchor = W ).grid(column = 1, row = 0, padx = 200)
        self.frame4 = Frame(self.parent)
        self.frame4.columnconfigure(3, weight = 1)
        self.frame4.columnconfigure(5, weight = 1)
        self.frame4.columnconfigure(1, weight = 1)
        self.frame4.columnconfigure(7, weight = 1)
        self.frame4.rowconfigure(4, weight = 1)
        self.frame4.pack(fill = X, expand = 1, side = TOP )
        Label(self.frame4, text = 'Year: ', anchor = W,font = ("Helvetica", 10, 'bold'), fg = 'blue' ).grid(row = 0,column=0, pady = 7, sticky = W)
        Label(self.frame4, text = 'Principle Investigator: ', anchor = W,font = ("Helvetica", 10, 'bold'), fg = 'blue' ).grid(row = 1,column=0,pady = 7, sticky = W)
        Label(self.frame4, text = 'Funding Institution: ', anchor = W,font = ("Helvetica", 10, 'bold'), fg = 'blue' ).grid(row = 2,column=0,pady = 7, sticky = W)

        #I will come back here
        self.yearBoxValue = StringVar()
        self.yearBox = Combobox(self.frame4, textvariable = self.yearBoxValue)
        self.yearBox.grid(row = 0,column=1,pady = 7, sticky = W,padx = 15)
        self.InvestBoxValue = StringVar()
        self.InvestBox = Combobox(self.frame4, textvariable = self.InvestBoxValue)
        self.InvestBox.grid(row = 1,column=1,pady = 7, sticky = W,padx = 15)
        self.InstitBoxValue = StringVar()
        self.InstitBox = ttk.Combobox(self.frame4, textvariable = self.InstitBoxValue)
        self.InstitBox.grid(row = 2,column=1,pady = 7, sticky = W,padx = 15)

        self.scrollbar = Scrollbar(self.frame4, orient=VERTICAL) #Creating the scrollbar which will work together with Listbox
        self.listbox = Listbox(self.frame4, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)#Tell the scrollbar that its gonna be working with the ListBox
        self.scrollbar.grid(column = 6,row = 0, rowspan = 3,sticky = N+S)
        self.listbox.grid(column = 3,row = 0,rowspan = 3,columnspan = 3 ,sticky = N+E+S+W)

        Button(self.frame4, text = 'Display Project Titles',command = self.dispButton,font = ("Helvetica", 9, 'bold'), anchor = CENTER).grid(row = 4, column = 0, sticky = W,padx = 10, pady = 20)
        Button(self.frame4, text = 'Show Description',command = self.DescrButton, font = ("Helvetica", 9, 'bold'), anchor = CENTER).grid(row = 4, column = 5, sticky = W,padx = 10, pady = 20)
        Label(text = '"'* (self.frame1.winfo_screenwidth()/7)).pack(fill = X, expand = 1)
        self.frame5 = Frame(self.parent)
        self.frame5.columnconfigure(0, weight = 1)
        self.frame5.columnconfigure(1, weight = 1)
        self.frame5.columnconfigure(2, weight = 1)
        self.frame5.rowconfigure(0, weight = 1)
        self.frame5.pack(fill = BOTH, expand = 1,side = TOP)
        self.canvas1=Canvas(self.frame5,bg='#FFFFFF',width=800,height=300, scrollregion = (0,0,200,200),relief = GROOVE)
        self.canvas1.config(width = 820, height = 320)
        self.canvas1.grid(row = 0, column = 0,columnspan = 2, sticky = N+E+S+W,pady = 10,padx = 5)
        self.canvas2=Canvas(self.frame5,bg='#FFFFFF',width=200,height=500, scrollregion = (0,0,300,300),relief = GROOVE)
        self.vertical_scroll = Scrollbar(self.frame5,orient=VERTICAL)
        self.vertical_scroll.grid(row = 0, column = 3, sticky = N+S)
        self.vertical_scroll.config(command = self.canvas2.yview) #we tell it its gonna work with canvas2
        self.horizontal_scroll = Scrollbar(self.frame5,orient=HORIZONTAL)
        self.horizontal_scroll.grid(row = 1, column = 2, sticky = W+E)   #pack(side=RIGHT,fill=Y)
        self.horizontal_scroll.config(command = self.canvas2.xview)
        self.canvas2.config(yscrollcommand = self.vertical_scroll.set,xscrollcommand = self.horizontal_scroll.set )
        self.canvas2.config(width = 300, height = 300)
        self.canvas2.grid(row = 0, column = 2, sticky = N+E+S+W,pady = 10,padx = 5)





    def fetchButton(self):
        s = self.urlEntry.get() #Gets whatever we write in the URL entry box
        self.response = urllib2.urlopen(str(s)) # It opens and downloads the webpage
        self.soup = BeautifulSoup(self.response, 'html.parser') #It reads the source of the webpage, and after this we can play with it
        self.data= self.soup.find_all("li",{"class":"list-group-item"}) #tAke all the parts which contain info about the projects
        self.mainDict = {}
        self.Year = []
        self.Investigator = []
        self.Institution = []
        for title in self.data:
            allYears = title.find_all("p")[0].text #Gives the part where years are mentioned
            (startYear,endYear) = (int(allYears.split()[2]),int(allYears.split()[6])) #Take the years and convert them to int
            allInstitutions = title.find_all("p")[1].text #Gives the part witth ist...
            (inst,name_of_inst) = (allInstitutions.split(':\n')[0],allInstitutions.split(':\n')[1])
            q = str(title.find("h4").text) #Gives the title of the project each step
            allInvestigators = title.find_all("p")[2].text #Find the part of the investigators
            blabla = title.find_all("img")[0]['src'] #Finds the needed continuity of the picture link

            allTexts = title.find_all("p")[4].string
            self.mainDict[q.lstrip().rstrip()] = {}  #Creates dict inside the mainDict holding the name of the project
            self.mainDict[q.lstrip().rstrip()]['Years'] = (startYear,endYear) # Put the start/end years inside the dict of the project title
            self.mainDict[q.lstrip().rstrip()][str(inst.lstrip().rstrip())] = str(name_of_inst.lstrip().rstrip()) #Put the name of institution inside the Project title dict
            self.mainDict[q.lstrip().rstrip()]['Text'] = allTexts #Put the text inside the project title dict
            self.mainDict[q.lstrip().rstrip()]['src'] = blabla #Put the image url inside the same dict
            self.mainDict[q.lstrip().rstrip()][str(allInvestigators.split('\n')[2].lstrip().rstrip())] = str(allInvestigators.split('\n')[5].lstrip().rstrip())#Put investigators name inside the same dict
            for year in (startYear,endYear):
                if year not in self.Year:  #In order to not put a YEAR twice or 3 times, only once
                    self.Year.append(year)
            if name_of_inst not in self.Institution: #Same for institution
                self.Institution.append(name_of_inst)
            if str(allInvestigators.split('\n')[5].lstrip().rstrip()) not in self.Investigator: # Same for Investigators
                self.Investigator.append(str(allInvestigators.split('\n')[5].lstrip().rstrip()))
        self.yearBox['values'] =['All Years'] + sorted(self.Year)
        self.yearBox.current(0)
        self.InvestBox['values'] = ['All Investigators'] + sorted(self.Investigator)
        self.InvestBox.current(0)
        self.InstitBox['values'] = ['All Institutions'] + sorted(self.Institution)
        self.InstitBox.current(0)


    def dispButton(self):
        self.res1 = []
        self.res2 = []
        self.res3 = []

        if self.yearBoxValue.get() == 'All Years':
            for key in self.mainDict.keys():
                self.res1.append(key)
        else:
            for key in self.mainDict.keys():
                (x,y) = self.mainDict[key]['Years']   #It checks every title, and gets the start/end years of every title, if what we
                                                # have selected is in between these years, we append the title to our first lis
                if x<= int(self.yearBoxValue.get()) <= y:
                    self.res1.append(key)



        if self.InvestBoxValue.get() == 'All Investigators':
            for key in self.mainDict.keys():
                self.res2.append(key)
        else:
            for key in self.mainDict.keys():
                if self.InvestBoxValue.get() == self.mainDict[key]['Principal Investigator:']:
                    self.res2.append(key)


        if self.InstitBoxValue.get() == 'All Institutions':
            for key in self.mainDict.keys():
                self.res3.append(key)
        else:
            for key in self.mainDict.keys():
                if str(self.InstitBoxValue.get().lstrip().rstrip()) == str(self.mainDict[key]['Funding Institution']):
                    self.res3.append(key)


        self.finalRes = list(set(self.res1) & set(self.res2) & set(self.res3)) #Find the intersection of the 3 lists by converting them to sets first, and to list afterwards
        self.listbox.delete(0, END)
        for val in self.finalRes: #We simply insert the final values(titles) into the ListBox
            self.listbox.insert(END, val)
    def DescrButton(self):

        self.index = int(self.listbox.curselection()[0])
        self.value =self.listbox.get(self.index) #We get what we have selected from Listbox
        print(self.value)
        self.myStr = ''
        self.canvas2.delete("all")
        self.canvas_text = self.canvas2.create_text(0,0, anchor = NW)
        self.myL = list(str(self.mainDict[self.value]['Text']))
        self.counter = 0
        for i in self.myL:
            if i == ' ' or i == ',' or i == '.':
                self.counter +=1
            if self.counter == 11:
                self.myStr +=  i + '\n'
                self.counter = 0
            else:
                self.myStr +=  i
        self.canvas2.itemconfig(self.canvas_text, text = self.myStr )
        self.draw()

    def draw(self):
        url = self.urlEntry.get()[0:23] + str(self.mainDict[self.value]['src'])[1:]
        print(url,type(url))
        image_bytes = urllib2.urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        #print data_stream
        pil_image = Image.open(data_stream)
        #print pil_image
        tk_image = ImageTk.PhotoImage(pil_image)
        #print tk_image
        self.canvas1.create_image(0, 0, image=tk_image, anchor='nw')
        #print 'done'

#{"class":"img-responsive img-thumbnail small-gap"}












def main():



    root = Tk()
    app = Proj4(root)
    app.winfo_geometry()
    root.rowconfigure(0, weight=5)
    root.columnconfigure(0, weight=5)
    root.mainloop()

main()