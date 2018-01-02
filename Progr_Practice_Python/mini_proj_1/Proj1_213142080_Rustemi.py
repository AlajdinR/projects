from Tkinter import *
from xlrd import open_workbook
import ttk
import tkFileDialog
import tkMessageBox
from os import *
import anydbm
import pickle

class Project(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        self.parent = parent
        self.frame1 = Frame(parent, height = 20)
        self.frame2 = Frame(parent, height = 20)
        self.label1 = Label (parent,text = "Curriculum Viewer v1.0", bg = "green", fg = "white")
        self.label2 = Label (self.frame1,text = "Please Select curriculum excel file: ", anchor = E)
        self.label3 = Label (self.frame1,text = "Please select semester that you want to print: ", anchor = E)
        self.LB0 = 'Semester'
        self.LB1 = 'Abbreviations: T (Theory), P (Practice), Cr (Credit), ECTS credit'
        self.LB2 = 'No. of Courses'

        self.but1 = Button(self.frame1, text = "Browse", command = self.browse_but)
        self.but2 = Button(self.frame1, text = "Display", command = self.disp_but)
        self.semesters = ttk.Combobox(self.frame1)
        self.semesters['values'] = ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI", "Semester VII", "Semester VIII"]
        self.semesters.current(0)

        self.interface(parent)


    def interface(self,parent):
        self.label1.pack(fill = BOTH, expand = True)
        self.frame1.pack(fill= BOTH, expand = True)
        self.label2.grid(row = 0, column = 0, sticky = E, padx = 10)
        self.label3.grid(row = 1, column = 0, sticky = E, padx = 10)
        self.frame1.grid_columnconfigure(0, weight = 10)
        self.but1.grid(row = 0, column = 1, sticky = W)
        self.semesters.grid(row = 1, column = 1)
        self.but2.grid(column = 1,sticky = E+W,padx = 10)


    def browse_but(self):
        self.importedFile = tkFileDialog.askopenfilename()
        self.currentFile = open_workbook(self.importedFile)
        print(self.currentFile.sheet_names())
        self.sheet = self.currentFile.sheet_by_index(0)
        self.save_work()

    def find_Semester_pos(self,semester):
        #self.whichSemester = self.semesters.get()
        for roww in range(self.sheet.nrows):
            for coll in range(self.sheet.ncols):
                if self.sheet.cell(roww,coll).value == semester:
                    self.coo_Row = roww
                    self.coo_Col = coll
        self.counter = 0
        for rows in range(self.coo_Row+1, self.sheet.nrows):
            if not(self.sheet.cell_value(rows,self.coo_Col).startswith(self.LB0) or self.sheet.cell_value(rows,self.coo_Col).startswith(self.LB1) or self.sheet.cell_value(rows,self.coo_Col).startswith(self.LB2)):
                self.counter += 1
            else:
                self.jump = self.counter
                break
        self.put_inList()


    def put_inList(self):
        self.list = []
        self.A = []
        self.ex = [0, 1, 5]
        for i in self.ex:
            self.list = self.list + self.sheet.col_slice(self.coo_Col + i,self.coo_Row +1, self.coo_Row + 1 + self.jump)
        for x in self.list:
            self.A.append(x.value)




    def save_work(self):
        self.db = anydbm.open("curriculum.db", "c")
        for sem in self.semesters['values']:
            self.find_Semester_pos(sem)
            self.db[sem] = pickle.dumps(self.A)
        self.db.close()

    def load_work(self):
        self.db = anydbm.open("curriculum.db", "c")
        self.loaded = pickle.loads(self.db[self.semesters.get()])
        self.db.close()

    def create_labels(self):
        self.frame2.destroy()
        self.frame2 = Frame()
        self.frame2.pack(fill = NONE, expand = False, anchor = W)
        self.mainn = 0
        for i in range(3):
            for ii in range(len(self.loaded)/3):
                if self.loaded[self.mainn] == '':
                    self.mainn += 1
                    continue
                else:
                    if self.loaded[self.mainn] == 'Semester Total =':
                        self.grid_forget()
                        Label(self.frame2, text = self.loaded[self.mainn],padx = 5, anchor = W).grid(row = self.mainn%(len(self.loaded)/3) , column = i, sticky = E, padx = 25, pady = 5)
                        self.mainn += 1
                    else:
                        self.grid_forget()
                        Label(self.frame2, text = self.loaded[self.mainn], padx = 5, anchor = W).grid(row = self.mainn%(len(self.loaded)/3) , column = i, sticky = W, padx = 25, pady = 5)
                        self.mainn += 1




    def disp_but(self):
        self.db = anydbm.open("curriculum.db", "c")
        if self.semesters.get() in self.db:
            self.load_work()
            self.create_labels()
        else:
            tkMessageBox.showwarning("Warning", "You didn't select any Excel file yet!!")










if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Curriculum Viewer v1.0')  # Set GUI Title
    root.geometry('{}x{}'.format('600', '190'))  # Set GUI geometry
    app = Project(root)  # Starting our app
    root.mainloop()  # Show GUI to user