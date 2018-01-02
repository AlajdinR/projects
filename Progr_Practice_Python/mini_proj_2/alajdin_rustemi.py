from tkinter import *
import tkinter.font as tkFont
from xlrd import open_workbook
import tkinter.ttk
import tkinter.messagebox as tkMessageBox
from os import *
import dbm as anydbm
from math import sqrt
import pickle
from recommendations import *
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')






class MainP(Frame):
    #This is the initialisation of the Class MainP. Here we call all the main function which will create the bases of our application,
    #and we open the needed files to start healthy our app
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        self.parent = parent
        self.menu = open_workbook("Menu.xlsx")
        #self.main_D_Meals()
        self.interface(parent)
        self.owndb = anydbm.open("ownratings.db", 'c').close()
        try:
            self.owndb = anydbm.open("ownratings.db", 'c')
            self.myDict =pickle.loads(self.owndb["MySelf"])
            for key in self.myDict.keys():
                self.theList1.insert(END, key+'-->'+str(self.myDict[key]))
            self.owndb["MySelf"] = pickle.dumps(self.myDict)
            self.owndb.close()
        except:
            self.myDict = dict()
            pass




    # Here we have nothing more than a bunch of code which creates most of the Interace required for s to create
    def interface(self,parent):
        self.text = 'm'
        Label(text = "Cafe Crown Recommendation Engine-SEHIR Special Edition", bg = "black", fg = "yellow",font = ("Helvetica", 15,"bold"),  anchor = CENTER,height = 2 ).pack(fill = X, expand = 0)
        Label(text = "Wellcome! \n Please rate entries that you have had at CC, and we will recommend you what you may like to have!", font = ("times", 13), height = 2).pack(fill = X, expand = 0, anchor = CENTER)
        Label(text = (self.winfo_screenwidth()/tkFont.Font(family = "Consolas", size = 12, weight = "normal").measure(self.text)) * '"', anchor = CENTER).pack(fill = X, expand = 1)
        #We firstly divide the program that we want to build into 3 main frames inside the "parent" frame we have:
        self.frame1 = Frame(parent)
        self.frame1.pack(fill = X, expand = True)
        Label(text = (self.winfo_screenwidth()/tkFont.Font(family = "Consolas", size = 12, weight = "normal").measure(self.text)) * '"', anchor = CENTER).pack(fill = X, expand = 0)
        Label(text = "Get Recommendations", anchor = CENTER, font = ("times", 15,"bold")).pack(fill = X, expand = 0)
        Label(text = (self.winfo_screenwidth()/tkFont.Font(family = "Consolas", size = 12, weight = "normal").measure(self.text)) * '"', anchor = CENTER).pack(fill = X, expand = 0)

        self.frame5 = Frame(parent)
        self.frame5.pack(fill = X, expand = True)
        Label(text = (self.winfo_screenwidth()/tkFont.Font(family = "Consolas", size = 12, weight = "normal").measure(self.text)) * '"', anchor = CENTER).pack(fill = X, expand = 0)
        self.frame9 = Frame(parent)

        #Now let's  deal with frame1, and create new framses and Labels inside of it:
        self.frame2 = Frame(self.frame1)
        self.frame2.pack(fill = Y, expand = 1, side = LEFT)
        self.frame3 = Frame(self.frame1)
        self.frame3.pack(fill = Y, expand = 1, side = LEFT)
        self.frame4 = Frame(self.frame1)
        self.frame4.pack(fill = BOTH, expand = 1, side = RIGHT)
        Label(self.frame2, text = "Choose a meal: ", fg = "dark red", anchor = W, font = ("Helvetica", 12, "bold")).pack(fill = BOTH,expand = 1, side = TOP)

        self.ch_meal_box(self.frame2)
        Label(self.frame3, text = "Enter your rating ", fg = "dark red", anchor = W, font = ("Helvetica", 12, "bold")).pack(fill = X, expand = 1, side = TOP)
        self.scale = Scale(self.frame3, from_ = 1, to = 10, orient = HORIZONTAL)
        self.scale.pack(fill = BOTH, expand = 1, side = BOTTOM, pady = 20, padx = 10)
        #We might change some stuff here(Buttons)

        Button(self.frame4, text = "Add ", anchor = S,command = self.add_Button , font = ("times", 12, "bold"), fg = "blue", width = 4).pack(side = LEFT, fill = X,expand = 1, padx = 10)
        self.scrollbar1 = Scrollbar(self.frame4)#First ListBox together with the scrollbar
        self.theList1 = Listbox(self.frame4, yscrollcommand = self.scrollbar1.set, width = 30)
        self.scrollbar1.config(command = self.theList1.yview)
        self.theList1.pack(side = LEFT, fill = BOTH, padx = 5)
        self.scrollbar1.pack(side = LEFT, fill = Y)

        Button(self.frame4, text = "Remove \nSelected", font = ("times", 12, "bold"), fg = "red", width = 8, command = self.remove_Button).pack(side = LEFT, fill = X, expand = 0, padx = 5)

        #Now let's deal with frame5 and creation of other widgets inside of it
        self.frame6 = Frame(self.frame5)
        self.frame6.pack(fill = BOTH, expand = 0,side = LEFT, anchor = W)
        self.frameB = Frame(self.frame5)
        self.frameB.pack(fill = BOTH, expand = 0, side = RIGHT)
        self.frame7 = Frame(self.frameB)
        self.frame7.pack(fill = BOTH, expand = 0, side = TOP)
        self.frame8 = Frame(self.frameB)
        self.frame8.pack(fill = BOTH, expand = 0, side = BOTTOM)
        Label(self.frame6, text = "Settings: ", fg = "red", font = ("times", 20, "bold"), anchor = W).grid(column = 0,row =0, sticky = W)
        Label(self.frame6, text = "Number of recommendations: ",font = ("times", 12) , anchor = W).grid(column = 0, row = 1)
        self.var0 = IntVar()
        self.entry = Entry(self.frame6, width = 3, textvariable = self.var0)
        self.entry.grid(column = 1, row = 1)
        self.var1 = IntVar()
        Label(self.frame7, text = "Choose Recommendation Method: ", fg = "deep pink", font = ("Helvetica", 10), anchor = W).grid(row = 1, column = 0, sticky = E)
        Radiobutton(self.frame7, text = "User-Based",font = ("Helvetica", 8,"bold"),variable = self.var1,  value = 0).grid(row = 2 , column = 0, sticky = W)
        Radiobutton(self.frame7, text = "Item-Based",font = ("Helvetica", 8,"bold"),variable = self.var1,  value = 1).grid(row = 3, column = 0, sticky = W)
        # Now the second group of RadioButtons
        self.var2 = StringVar()
        self.var2.set('sim_pearson')
        Label(self.frame8, text = "Choose Similarity Metric: ", fg = "deep pink", font = ("Helvetica", 11), anchor = W).grid(row = 0, column = 0)
        Radiobutton(self.frame8, text = "Euclidian Score",font = ("Helvetica", 8,"bold"),variable = self.var2, value = 'sim_distance').grid(row = 1, column = 0, sticky = W)
        Radiobutton(self.frame8, text = "Pearson Score",font = ("Helvetica", 8,"bold"),variable = self.var2,  value = 'sim_pearson').grid(row = 2, column = 0, sticky = W)
        Radiobutton(self.frame8, text = "Jaccard Score",font = ("Helvetica", 8,"bold"),variable = self.var2, value = 'sim_jaccard').grid(row = 3, column = 0, sticky = W)
        #Might be wrong ,still need to come back BUTTON
        Button(self.frame8, text = "Get Recommendations", anchor = N, font = ("times", 12, "bold"), fg = "blue", command = self.getRec_Button).grid(row = 2, column = 1, padx = 10)
        #Label(text = (self.winfo_screenwidth()/tkFont.Font(family = "Consolas", size = 12, weight = "normal").measure(self.text)) * '"', anchor = CENTER).pack(fill = X, expand = 1)




    #Third part of the interface. It doesn't show immidiately, but it shows after we have chosen in which method we will work
    def interface_2(self,parent, method):
        self.frame9.destroy()
        self.frame9 = Frame(parent)
        self.frame9.pack(fill = X, expand = True)
        #Here we deal with the 3rd main part. We will create another frames and other widgets here
        Label(self.frame9, text = "Result Box(Recommendations): ", anchor = W, font = ("times", 12)).grid(column = 0, row = 0,sticky = N)
        self.frame10 = Frame(self.frame9)
        self.frame10.grid(column = 0, row = 1)
        self.scrollbar2 = Scrollbar(self.frame10)
        self.theList2 = Listbox(self.frame10, yscrollcommand = self.scrollbar2.set, width = 30, height = 7)
        self.scrollbar2.config(command = self.theList2.yview)
        self.theList2.pack(side = LEFT, fill = BOTH, padx = 5)
        self.scrollbar2.pack(side = LEFT, fill = Y)
        self.frame11 = Frame(self.frame9)
        self.scrollbar3 = Scrollbar(self.frame11)
        self.theList3 = Listbox(self.frame11, yscrollcommand = self.scrollbar3.set, width = 30, height = 7)
        self.frame12 = Frame(self.frame9)
        self.scrollbar4 = Scrollbar(self.frame12)
        self.theList4 = Listbox(self.frame12, yscrollcommand = self.scrollbar4.set, width = 30, height = 7)
        if method == 0:
            self.frame11.forget()
            self.frame11.grid(column = 1, row = 1)
            Label(self.frame11, text = "Users similar to you", bg = "purple", font = ("times", 9,"bold"), fg = "white" ).pack(fill = X, expand = 0, side = TOP, padx = 4)


            self.scrollbar3.config(command = self.theList3.yview)
            self.scrollbar3.pack(side = RIGHT, fill = Y)
            self.theList3.bind("<<ListboxSelect>>", self.select_box0)
            self.theList3.pack(side = RIGHT, fill = BOTH, padx = 5)

            self.frame12.grid(row = 1, column = 2)
            Label(self.frame12, text = "Users ratings(Select a user on the left)", bg = "dark red", font = ("times", 8,"bold"), fg = "white" ).pack(fill = X, expand = 0, side = TOP, anchor = E, padx = 5)


            self.scrollbar4.config(command = self.theList4.yview)
            self.scrollbar4.pack(side = RIGHT, fill = Y)
            self.theList4.pack(side = RIGHT, fill = BOTH, padx = 8)
        elif method == 1:
            self.frame11.grid(column = 1, row = 1)
            Label(self.frame11, text = "Original Ratings", bg = "purple", font = ("times", 9,"bold"), fg = "white" ).pack(fill = BOTH, expand = 0, side = TOP, padx = 5)

            self.scrollbar3.config(command = self.theList3.yview)
            self.scrollbar3.pack(side = RIGHT, fill = Y)
            self.theList3.bind("<<ListboxSelect>>", self.select_box1)
            self.theList3.pack(side = RIGHT, fill = BOTH, padx = 3)

            self.frame12.grid(row = 1, column = 2)
            Label(self.frame12, text = "Similar items(Select an item on the left)", bg = "dark red", font = ("times", 8,"bold"), fg = "white" ).pack(fill = BOTH, expand = 0, side = TOP, anchor = E, padx = 10)

            self.scrollbar4.config(command = self.theList4.yview)
            self.scrollbar4.pack(side = RIGHT, fill = Y)
            self.theList4.pack(side = RIGHT, fill = BOTH, padx = 8)





    #Here all what we do is take the data of food names and their prices from the provided excell file,
    #Then we put these data and put it in a dictionary.Then we simply populate the combobox.
    def ch_meal_box(self, parent):
        self.sheet = self.menu.sheet_by_index(0)
        self.ch_value = StringVar()
        self.combobox = ttk.Combobox(parent, textvariable = self.ch_value)
        self.combobox['values'] = [self.sheet.cell(num,0).value for num in range(1,self.sheet.nrows)]
        self.combobox.current(0)
        self.combobox.pack(fill = X, expand = 1, side = BOTTOM, pady = 25)
        return self.combobox





    #Here we create a function which is going to be called in the event when we click a line on the Middle ListBox
    #This function is called in the event when we have User-Based case
    #It will list whatever the people similar to us have chosen and rated
    def select_box0(self, event):
        try:
            self.widget = event.widget
            self.value = self.widget.get(self.widget.curselection())
            self.person = self.value.split('-')[1]
            self.theList4.delete(0, END)
            self.theList4.insert(END, "%s has also rated the following: "% self.person)
            self.theList4.insert(END, "  ")
            for item in self.bigDict[self.person].keys():
                self.theList4.insert(END, '%s --> %d'%(item, self.bigDict[self.person][item]))
        except:
            tkMessageBox.showwarning('Warning', 'The ListBox is empty')





    #Here we create a function which is going to be called in the event when we click a line on the Middle ListBox
    #This function is called in the event when we have Item-Based case
    def select_box1(self, event):

        self.widget = event.widget
        self.value = self.widget.get(self.widget.curselection())
        self.item = self.value.split('-->')[0]
        self.similar_items = calculateSimilarItems(self.bigDict)
        self.theList4.delete(0, END)
        for rating,article in self.similar_items[self.item]:
            self.theList4.insert(END,'%g-->%s'%(round(rating,2), article))






    #This function is called when the 'Add' button is pressed
    #It load whatever was previously saved in our anydbm file(if there was anything) and puts everythin in a dictionary
    #We Get the value from combobox as key for the same dictionary(myDict) and the scale value as the value of the dictionary
    def add_Button(self):
        self.owndb = anydbm.open("ownratings.db", 'c')
        try:
            self.myDict =pickle.loads(self.owndb["MySelf"])
        except:
            self.owndb['MySelf'] = pickle.dumps({})
            self.myDict =pickle.loads(self.owndb["MySelf"])
        self.myDict[self.ch_value.get()] = self.scale.get()#Here we put new chosen items in the dictionary
        self.theList1.delete(0,END) #We allways delete everything in the list before updating it
        for key in self.myDict.keys():
            self.theList1.insert(END, key+'-->'+str(self.myDict[key])) #Updating the List
        self.owndb["MySelf"] = pickle.dumps(self.myDict) #Saving the dictionary in the same anydbm database
        self.owndb.close()





    #This function is called when the 'Remove' button is pressed. It firstly reloads the saved data from anydbm database
    #to the myDict dictionary. It gets whatever item is selected from the list. Afterwards, the same item from the dictionary.
    #Then it puts again everything in the listbox(The deleted item is NOT there). It then saves the dictionary again in database,
    #and closes the database
    def remove_Button(self):
        self.owndb = anydbm.open("ownratings.db", 'c')
        self.myDict =pickle.loads(self.owndb["MySelf"])
        self.get_list_selection = self.theList1.get(ACTIVE)
        self.item_value = self.get_list_selection.split('-->')
        try:
            del self.myDict[self.item_value[0]]
        except: tkMessageBox.showwarning("Warning", "There is nothing left to Delete !")
        self.theList1.delete(0,END)
        for item in self.myDict:
            self.theList1.insert(END, item+'-->'+str(self.myDict[item]))
        self.owndb["MySelf"] = pickle.dumps(self.myDict)

        self.owndb.close()






    #This function is called when the 'Get Recommendation' button is pressed.
    #It gather the data from both databases(the one we create and the one provided by the instructor) into one single dictionary,
    #which will be used inside the provided recommendation functions latter on in the same function
    def getRec_Button(self):
        self.bigDict = dict()
        self.owndb = anydbm.open("ownratings.db", 'c')
        self.otherdb = anydbm.open("cc_ratings.db", 'c')

        for key in self.otherdb.keys():
            self.bigDict[key] = pickle.loads(self.otherdb[key])
        for keyy in self.owndb.keys():
            self.bigDict[keyy] = pickle.loads(self.owndb[keyy])
        self.otherdb.close() #After gathering everything in the bigDict dictionary, we close one of the databases,however,
                             #we leave the other one still open as we might need it afterwards
        self.num_rec = int(self.entry.get()) #It gets the number that we provide as the Number of Recommendations
        self.method = self.var1.get()  #It sees what we choose as recommendation method(User-based or Item-Based)
        self.similarityy = self.var2.get() # Here we get the metric that we want to use, but as a string(not a function)
        self.interface_2(self.parent, self.method) #Here we call the missing part(3rd part of the interface)
        self.theList2.insert(END, "Similarity Score-->Recommendation")
        if self.method == 0: #It means we are dealing with User-Based Recommendations
            self.owndb.close() #If User-Based, we don't need anymore the data-base we created, so we close it
            self.rankings0 = getRecommendations(self.bigDict,'MySelf', eval(self.similarityy) )
            if self.rankings0 == []:
                tkMessageBox.showwarning("Warning", "Not enough items rated for using %s Similarity Metric" %(self.similarityy))
            for score, item in self.rankings0:
                self.theList2.insert(END,'%g-->%s'%(round(score,2), item ))

            self.simPpl = topMatches(self.bigDict,'MySelf',similarity=eval(self.similarityy), n = self.num_rec)
            for sccore, people in self.simPpl:
                self.theList3.insert(END, '%g-%s'%(round(sccore,2), people)) #simply filling the middle List
        elif self.method == 1: #It means we are dealing with Item-Based Recommendations
            try:
                self.reverse = transformPrefs(self.bigDict)
                self.sim_items = calculateSimilarItems(self.bigDict)
                self.rankings1 = getRecommendedItems(self.bigDict, self.sim_items, 'MySelf')
                for score, item in self.rankings1:
                    self.theList2.insert(END,'%g-->%s'%(round(score,2), item ))
                for k in self.owndb:
                    self.myDict =pickle.loads(self.owndb[k])
                for key in self.myDict.keys():
                    self.theList3.insert(END, key+'-->'+str(self.myDict[key])) #simply filling the middle List
                self.owndb.close() #If Item-Based, we close our created database at the end
            except: tkMessageBox.showwarning("Warning", "Not enough items rated for using Item-Based Recommendation")







def main():

    root = Tk()
    root.title('Enter the Recommender')
    app = MainP(root)
    app.winfo_geometry()
    root.mainloop()

main()