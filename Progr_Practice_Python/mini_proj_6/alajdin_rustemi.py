
"""
 Alajdin Rustemi
 St.Number: 213142080

"""
from xlrd import open_workbook
import ttk
import tkFileDialog
from Tkinter import *  # Python 2
from tkMessageBox import showerror, showwarning  # Python 2
from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import re
import shelve
import time
import ScrolledText
from docclass import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class GuessMyGrade(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #All Variables
        self.LB0 = 'Semester'
        self.LB1 = 'Abbreviations: T (Theory), P (Practice), Cr (Credit), ECTS credit'
        self.LB2 = 'No. of Courses'
        self.semesters_pos = {}



        #All frames defined
        self.upperFrame = Frame(self.root)
        self.midFrame = Frame(self.root)
        self.lowerFrame = Frame(self.root)



        #All Labels
        self.title = Label(self.upperFrame, text="Guess My Grade! v1.0", bg="black", fg="white",
                           font=('Comic Sans', 18, 'bold'), height=1)
        self.browsLabel = Label(self.upperFrame, text = 'Please upload your curriculum file with the grades: ', fg = "blue", font = ('Comic Sans', 12, 'bold'))
        self.urlsLabel = Label(self.midFrame, text = 'Enter urls for course descriptions', fg = 'black',font = ('Comic Sans', 12) )
        self.Key = Label(self.midFrame, text = 'Key: ',font = ('Comic Sans', 12, 'bold'), anchor = W )
        self.A = Label(self.midFrame, text = ' A ', font = ('Comic Sans', 12), fg = 'white', bg = 'dark green',width = 10)
        self.B = Label(self.midFrame, text = ' B ', font = ('Comic Sans', 12), fg = 'white', bg = 'pale green',width = 10)
        self.C = Label(self.midFrame, text = ' C ', font = ('Comic Sans', 12), fg = 'white', bg = 'orange',width = 10)
        self.D = Label(self.midFrame, text = ' D ', font = ('Comic Sans', 12), fg = 'white', bg = 'red',width = 10)
        self.F = Label(self.midFrame, text = ' F ', font = ('Comic Sans', 12), fg = 'white', bg = 'black',width = 10)
        self.preGr = Label(self.lowerFrame,text = 'Predicted Grades ', font = ('Comic Sans', 13, 'bold') ,width = 10, anchor = W)
        self.divLine1 = Label(self.upperFrame, text = '--'* 80) #Left here
        self.divLine2 = Label(self.midFrame, text = '--'* 80)

        #All Buttons
        self.browse = Button(self.upperFrame,command = self._browse_but, text = 'Browse',font = ('Comic Sans', 12), fg = 'white', bg = 'firebrick', width = 20 )
        self.predGrades = Button(self.midFrame,command = self.kot, text = 'Predict Grades',font = ('Comic Sans', 12), fg = 'white', bg = 'firebrick', width = 18 )

        #All text and entries
        self.urlinput = Listbox(self.midFrame, height = 8, width = 100,bg ='gray',font = ('Comic Sans', 8)) #wrap = 'word',
        self.resultText = ScrolledText.ScrolledText(self.lowerFrame, wrap = 'word',height =16,font = ('Comic Sans', 10) )

        self._interface()



    def _interface(self):
        #All Frames
        self.upperFrame.grid(row = 0, sticky = E+W)
        self.upperFrame.columnconfigure(0, weight = 1)
        self.midFrame.grid(row = 1, pady = 10,sticky = E+W)
        self.lowerFrame.grid(row = 2,pady = 10,sticky = W+E)
        self.lowerFrame.columnconfigure(0,weight = 1)

        #Upper Frame
        self.title.grid(row = 0, columnspan = 2, sticky = E+W)
        self.browsLabel.grid(row = 1, column = 0, sticky = W, pady = 10)
        self.browse.grid(row = 1, column = 1, padx = 70, sticky = E+W, pady = 10)
        self.divLine1.grid(row = 2, columnspan = 2, sticky = E+W)

        #Mid Frame
        self.urlsLabel.grid(row = 0, column = 0, columnspan = 7, sticky = W)
        self.urlinput.grid(row = 1, column = 0, columnspan = 6, sticky = W)
        self.Key.grid(row = 2, sticky = W)
        self.A.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = W)
        self.B.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W+E)
        self.C.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = W+E)
        self.D.grid(row = 3, column = 3, padx = 5, pady = 5, sticky = W+E)
        self.F.grid(row = 3, column = 4, padx = 5, pady = 5, sticky = W+E)
        self.predGrades.grid(row = 3, column = 5, columnspan = 2, padx = 30, sticky = W+E,pady = 5)
        self.divLine2.grid(row = 4, columnspan = 7)

        #Lower Frame
        self.preGr.grid(row = 0, sticky = W+E,padx = 10)
        self.resultText.grid(row = 1, sticky = W + E + S + N)


    def _browse_but(self):
        self.importedFile = tkFileDialog.askopenfilename()
        #try:
        self.currentFile = open_workbook(self.importedFile)
        self.sheet = self.currentFile.sheet_by_index(0)
        print self.find_Semester_pos()
        #except: pass

        #print(self.currentFile.sheet_names())

    def find_Semester_pos(self):
        department = None
        for roww in range(self.sheet.nrows):
            try:
                department = self.sheet.cell_value(roww, 0).split('-')[1].strip().lower()
            except: pass
            for coll in range(self.sheet.ncols):
                if str(self.sheet.cell(roww,coll).value).startswith('Semester') and not str(self.sheet.cell(roww,coll).value).startswith('Semester Total'):
                    a = str(self.sheet.cell(roww,coll).value)
                    if str(self.sheet.cell(roww + 2,coll + 6).value) == '':
                        self.semesters_pos[a] = ((roww, coll), 'not taken')
                    else: self.semesters_pos[a] = ((roww, coll), 'taken')
                else:pass
        return department



    def kot(self):
        b = self.semesters_pos
        print b.items()
        a = self.find_Semester_pos()
        print a


    def put_inList(self):
        self.list = []
        self.A = []
        self.ex = [0, 1, 5]
        for i in self.ex:
            self.list = self.list + self.sheet.col_slice(self.coo_Col + i,self.coo_Row +1, self.coo_Row + 1 + self.jump)
        for x in self.list:
            self.A.append(str(x.value))
        print self.list
        print self.A





    def go_through_excel(self):
        pass

        def find_courses(semester_loc):
            pass

        def find_grades(course_loc):
            pass

        def finished_notFinished(semester):
            pass




    #When we get to the provided pages, after ldownloading and souping them, we have to go through the course descr texts, and decide to which grade category
    # this text corresponds, and according to that , the course having this descr will correspond to that grade.

    #We first need to train our machine with the courses we have already taken


    def go_through_pages(self):
        pass

        def find_course_descr(course):
            pass







if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Guess My Grade')  # Set GUI Title
    root.geometry('{}x{}+250+0'.format('800', '600'))  # Set GUI geometry
    app = GuessMyGrade(root)  # Starting our app and passing tables to our app.
    root.mainloop()  # Show GUI to user