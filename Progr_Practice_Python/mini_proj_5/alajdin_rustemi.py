from Tkinter import *
from PIL import Image, ImageTk
from ttk import Combobox
import tkFileDialog, tkMessageBox, os, pickle, anydbm
from math import sqrt
import ttk
import urllib2
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import io
import shelve
from django.utils.encoding import smart_str
from urlparse import urljoin
import operator
import time




class Proj5(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        self.parent = parent
        self.parent.title('SEHIR Reserh Projects Analyzer ')
        ttk.Style().configure("TFrame", background="#F333")
        self.openshelve()
        self.interface(parent)
        self.pack()
        self.i = 1

    def interface(self,parent):

        Label(self.parent,text = 'SEHIR Scholar', bg = "Blue", fg = "white",height = 2,font = ("Helvetica", 16, 'bold'),anchor = CENTER).pack(fill = X, expand = 0,side = TOP)
        self.frame0 = Frame(self.parent, width = 100)
        self.frame0.columnconfigure(0, weight = 1)
        self.frame0.columnconfigure(2, weight = 1)
        self.frame0.columnconfigure(3, weight = 1)
        self.frame0.columnconfigure(4, weight = 1)
        self.frame0.columnconfigure(7, weight = 1)
        self.frame0.columnconfigure(9, weight = 1)
        Label(self.frame0, text = 'Url for faculty list :  ', font =('Helvetica',9,'bold')).grid(row = 0, column = 1, sticky = E)
        self.webpage = StringVar()
        self.urlEntry = Entry(self.frame0,bg = '#FFFFFF',textvariable = self.webpage)
        self.urlEntry.grid(column = 2, row = 0,columnspan = 4, padx = 10, pady = 10, sticky = W+E)
        Button(self.frame0, text = 'Build Index',command = self.indexButt, font =('Helvetica',9,'bold') ).grid(row = 0, column = 7,padx = 20 )
        self.myWord = StringVar()
        self.myEntry = Entry(self.frame0,bg = '#FFFFFF', textvariable = self.myWord)
        self.myEntry.grid(row = 1, column = 1, columnspan = 7, sticky = W+E, padx = 30,ipady = 5)
        Label(self.frame0, text = 'Ranking Criteria', font =('Helvetica', 10,'bold'),anchor = W).grid(column = 2, row = 2,columnspan = 2, sticky = W, padx = 10)
        Label(self.frame0, text = 'Weight', font =('Helvetica', 10,'bold'), anchor = W).grid(column = 4, row = 2, sticky = W+E, padx = 50)
        Label(self.frame0, text = 'Filter Papers', font =('Helvetica', 10,'bold'),anchor = E).grid(column = 5, row = 2,columnspan = 2, sticky = E, padx = 10)
        Button(self.frame0, text = 'Search',command = self.SearchButt,   anchor = CENTER,font =('Helvetica',9,'bold') ).grid(row = 3, column = 7,padx = 30)
        self.check1 = StringVar()
        Checkbutton(self.frame0, text="Word Frequency",font =('Sans',10,'bold'), variable=self.check1, onvalue = "freqScore", offvalue = 0).grid(row=3,column = 2, columnspan = 2, sticky=W)
        self.check1.set(0)
        self.check2 = StringVar()
        Checkbutton(self.frame0, text="Citation Count",font =('Sans',10,'bold'), variable=self.check2, onvalue = "citScore", offvalue = 0).grid(row=4,column = 2, columnspan = 2, sticky=W)
        self.check2.set(0)
        self.num1 = IntVar()
        Entry(self.frame0,bg = '#FFFFFF',textvariable = self.num1,width = 4).grid(row = 3, column = 4, sticky = W,padx = 50)
        self.num1.set(1)
        self.num2 = IntVar()
        Entry(self.frame0,bg = '#FFFFFF',textvariable = self.num2, width = 4).grid(row = 4, column = 4, sticky = W, padx = 50)
        self.num2.set(1)





        self.scrollbar = Scrollbar(self.frame0, orient=HORIZONTAL)
        self.listbox = Listbox(self.frame0, xscrollcommand=self.scrollbar.set,height = 5,selectmode = MULTIPLE)
        self.scrollbar.config(command=self.listbox.xview)
        self.scrollbar.grid(column = 5,row = 5, columnspan = 2,sticky = W+E)
        self.listbox.grid(column = 5,row = 3,rowspan = 2,columnspan = 2 ,sticky = N+E+S+W)


        self.scrollbar1 = Scrollbar(self.frame0, orient=VERTICAL)
        self.mainText = Text(self.frame0,yscrollcommand = self.scrollbar1.set)
        self.scrollbar1.config(command=self.mainText.yview)
        self.scrollbar1.grid(column = 8,row = 7,sticky = N+S+W)
        self.mainText.grid(row = 7, column = 1,columnspan = 7, sticky = W+E+S+N)

        Label(self.frame0, text = 'Page: ', font =('Helvetica',10,'bold')).grid(row = 8, column = 4, pady = 5, padx = 5, sticky = E)
        self.prevButt = Button(self.frame0,command = self.previousButton, text = 'Previous', font =('Helvetica',9,'bold') )
        self.prevButt.grid(row = 8, column = 5,padx = 10,pady = 5, sticky = E )
        self.prevButt.config(state = DISABLED)
        self.pgnum = IntVar()
        self.page =Entry(self.frame0,font =('Helvetica',9,'bold'),textvariable = self.pgnum, width = 5, bg = "blue", fg = "white")
        self.page.grid(row = 8, column = 6,padx = 5, pady = 5)
        self.pgnum.set(1)
        self.page.config(state = DISABLED)

        self.nexButt = Button(self.frame0,command = self.nextButton,  text = 'Next', font =('Helvetica',9,'bold'), width = 8 )
        self.nexButt.grid(row = 8, column = 7,padx = 10,pady = 5, sticky = W )
        self.nexButt.config(state = DISABLED)


        self.frame0.pack(fill = X, expand = 0, side = TOP)



    #This function gets a list which contains all the paper categories once only, and nserts them in the ListBox
    def populateLB(self, typelist):
        self.listbox.delete(0,END)
        for item in typelist:
            self.listbox.insert(END, item)
            self.listbox.select_set(0,END)

    #Its copied from mysearchengine.py
    def separatewords(self,text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']


    #It's important function. This function is the command for the Index Button. It fetches all the children webpages(urls) by going to the main url we give
    #in the beggining. It goes through each child url via urllib2 and BeautifulSoap. What it does shortly is go through every page, save the page string first in self.UrlList db,
    # then it finds all the papertypes, inside each papertype it finds all the words, it finds each word in which titles is used, and also saves the locations of each
    # word in each title of each child page.Thats done in another nested dict which I have explained bellow. And the third nested dict just goes through papertitles and finds the
    # citation number for each of them.Again here we have another dict. In total there are 3 shelve dbs(or dictionaries)
    def indexButt(self):
        self.openshelve()
        try:
            s = self.urlEntry.get() #Gets whatever we write in the URL entry box
            self.response = urllib2.urlopen(str(s)) # It opens and downloads the webpage
            self.soup = BeautifulSoup(self.response, 'html.parser')
            self.motherPage= self.soup.find_all("h4")
            self.listBoxInput = []
            self.D1 = dict()
            tempD = dict()
            for i in self.motherPage:
                newUrl = smart_str(urljoin(s,i.a['href']))
                self.urlList.setdefault(newUrl, 0)
                self.childPage = urllib2.urlopen(newUrl)
                self.soup2 = BeautifulSoup(self.childPage, 'html.parser')
                self.paperTypeList = self.soup2.find_all("div", {"id" : "publication"})[0].find_all('p')
                for elem in self.paperTypeList:
                    self.listBoxInput.append(smart_str(elem.string.strip()))
                self.populateLB(list(set(self.listBoxInput)))

                for i in range(len(self.paperTypeList)): #Basically goes through the papertype list by index
                    paperType = smart_str(self.paperTypeList[i].string.strip()) #Here we want to filter the paper TYPE as a string only and use it latter
                    if paperType not in tempD.keys():
                        tempD.setdefault(paperType, {})
                    else: pass

                    for paper_Title in self.soup2.find_all("div", {"id" : "publication"})[0].find_all('ul')[i].find_all("li"): #We go through each paperTitle in the corresponding subgroup of PaperTYPE
                        papertitle = smart_str(' '.join(paper_Title.text.split()[1:]))
                        if self.separatewords(papertitle)[-1] == 'citations' or self.separatewords(papertitle)[-1] == 'citation':
                            self.citationDict[papertitle] = float(self.separatewords(papertitle)[-2])
                            for loc, word in enumerate(self.separatewords(papertitle)[:-2]):
                                if word not in tempD[paperType].keys():
                                    tempD[paperType].setdefault(word, {})
                                else: pass
                                if papertitle not in tempD[paperType][word].keys():
                                    tempD[paperType][word][papertitle] = [loc]
                                else:
                                    tempD[paperType][word][papertitle].append(loc)
                        else:
                            self.citationDict[papertitle] = 0
                            for loc, word in enumerate(self.separatewords(papertitle)):
                                if word not in tempD[paperType].keys():
                                    tempD[paperType][word] = {}
                                if papertitle not in tempD[paperType][word].keys():
                                    tempD[paperType][word][papertitle] = [loc]
                                else:
                                    tempD[paperType][word][papertitle].append(loc)
            self.citationDict.close()
            for key in tempD.keys():
                self.wordLocation[key] = tempD[key]
            self.close()
        except: tkMessageBox.showwarning('Warning', "The URL you have provided is invalid, or you didn't provide one")







    #Here we get a list of the categories we have chosed from the listbox
    def getListboxitems(self):
        selCategories = []
        for sel in self.listbox.curselection():
            selCategories.append(self.listbox.get(sel))
        return selCategories


    #Just doing the pagination duty, dividing all the titles in groups of 10 in our case
    def getrows_byslice(self, seq, rowlen):
        for start in xrange(0, len(seq), rowlen):
            yield seq[start:start+rowlen]



    #Its the function for Search Button
    #It contains other functions inside, but mainly it goes through the data we have saved,and according to what weight and measue we have chosen,and what word we have typed,
    #it filters things up, and gives us the needed result
    def SearchButt(self):
        self.openshelve()
        self.mainText.delete('1.0', END)
        self.start_time = time.time()
        try:
            self.requirements = [( self.num1.get(),self.check1.get()),(self.num2.get() ,self.check2.get())]
        except:
            tkMessageBox.showwarning('', 'Please provide the weights for the ranking Measures')
            return
        self.category = self.getListboxitems()
        self.input_words = self.separatewords(self.myWord.get())
        self.results = self.getres()
        if self.check1.get()=='0' and self.check2.get()=='0':
            tkMessageBox.showwarning('', 'Choose at least one ranking measure!')
            return 0
        if self.results == 0:
            return 0
        else:
            self.final_res = self.getFinalscore()
        self.paginated_data = list(self.getrows_byslice(self.final_res,10))
        self.elapseTime = time.time() - self.start_time
        self.number = len(self.final_res)
        Label(self.frame0, text = '%d Publications(%.3f seconds)'%(self.number, self.elapseTime), font =('Sans', 12, 'bold'), fg = 'red').grid(column = 1, row = 6, columnspan = 6, sticky = W)
        self.txtInput()
        self.close()

    #Fun for the next Button . It allways checks the number in the entry(pg number) and accordingly disables itself or the other button
    def nextButton(self):
        self.page.config(state = NORMAL)
        counter = self.pgnum.get()
        self.pgnum.set(counter + 1)
        counter = self.pgnum.get()
        self.page.config(state = DISABLED)
        print self.pgnum.get()
        self.mainText.config(state = NORMAL)
        self.mainText.delete('1.0', END)
        ln = 1
        for data, score in self.paginated_data[counter - 1]:
            input_D = str(self.i)+'.'+'\t'+data+'\t'+str(score)+'\n'
            self.mainText.insert(END, input_D )
            self.location_list = self.findPos(input_D)
            for num in self.location_list:
                self.mainText.tag_add('success',str(ln)+'.'+str(num)+ 'wordstart', str(ln)+'.'+str(num +1)+ ' wordend')
            ln +=1
            self.i += 1
        self.mainText.config(state = DISABLED)
        self.prevButt.config(state = NORMAL)
        if self.pgnum.get() > len(self.paginated_data) -1 :
            self.nexButt.config(state = DISABLED)
        else: self.nexButt.config(state = NORMAL)
        return self.i


    #Fun for the previous Button . It allways checks the number in the entry(pg number) and accordingly disables itself or the other button
    def previousButton(self):
        self.page.config(state = NORMAL)
        counter = self.pgnum.get()
        self.pgnum.set(counter - 1)
        counter = self.pgnum.get()
        self.page.config(state = DISABLED)
        print self.pgnum.get()
        self.i = self.i - (10 + len(self.paginated_data[counter]))
        self.mainText.config(state = NORMAL)
        self.mainText.delete('1.0', END)
        ln = 1
        for data, score in self.paginated_data[counter - 1]:
            input_D = str(self.i)+'.'+'\t'+data+'\t'+str(score)+'\n'
            self.mainText.insert(END, input_D )
            self.location_list = self.findPos(input_D)
            for num in self.location_list:
                self.mainText.tag_add('success',str(ln)+'.'+str(num)+ 'wordstart', str(ln)+'.'+str(num +1)+ ' wordend')
            ln +=1
            self.i += 1
        self.mainText.config(state = DISABLED)
        self.nexButt.config(state = NORMAL)
        if self.pgnum.get() == 1:
            self.prevButt.config(state = DISABLED)
        return self.i


    #It is the first page that we see on Text widget after pressing Search. After this is shown , then we caan play with Next/Previous accordingly
    def txtInput(self):
        counter = self.pgnum.get()
        if len(self.paginated_data) > 1:
            self.nexButt.config(state = NORMAL)
        self.mainText.delete('1.0', END)
        self.mainText.tag_config("success", foreground="blue", font="Arial 10 italic")
        ln = 1
        for data, score in self.paginated_data[counter - 1]:
            input_D = str(self.i)+'.'+'\t'+data+'\t'+str(score)+'\n'
            self.mainText.insert(END, input_D )
            self.location_list = self.findPos(input_D)
            for num in self.location_list:
                self.mainText.tag_add('success',str(ln)+'.'+str(num)+ 'wordstart', str(ln)+'.'+str(num +1)+ ' wordend')
            ln +=1
            self.i += 1
        return self.i



#This function finds out where does each word we have looked for start in the text we have inputted in Text Widget(location by character)
    def findPos(self, dataa):
        L = list(dataa)
        loc_list = []
        for word in self.input_words:
            for i in range(len(L)-len(word)):
                self.stringg = ''
                for j in range(len(word)):
                    self.stringg = self.stringg + L[i + j]
                    if self.stringg.lower() == word:
                        loc_list.append(i)
                    else : pass
        return loc_list



    #Gets the final score we need ...a sorted list of tuples whch contain the title as a first arg and its final score as the second arg...the sorting is due due to second arg(score)

    def getFinalscore(self):
        self.totalscores = dict([(title,0) for title in self.results])
        weights =[]
        for  weight,scores in self.requirements:
            if scores != '0':
                weights.append((weight,scores))
            else: pass
        for weight,scores in weights:
            self.method = getattr(Proj5, scores)(self)
            for title in self.totalscores.keys():
                self.totalscores[title] += weight *self.method.get(title,0)
        norm_total = self.normalizescores(self.totalscores)
        sorted_norm = sorted(norm_total.items(), key=operator.itemgetter(1),reverse = True)
        return sorted_norm

    #Just looks for exceptions and gives us a list of all the titles that contain the word/s we are looking for
    def getres(self):
        self.res = []
        if not self.category:
            tkMessageBox.showwarning('', 'Choose at least one paper category ! ')
            return 0
        if not self.input_words:
            tkMessageBox.showwarning('', 'Provide at least one keyword !')
            return 0
        for cat in self.category:
                for myW in self.input_words:
                    if myW in self.wordLocation[cat].keys():
                        for title in self.wordLocation[cat][myW].keys():
                            self.res.append(title)
                    else: pass
        return list(set(self.res))

    #Its a modified version of frequency score
    def freqScore(self):
        self.freqcounts = {}
        for title in self.results:
            score = 1
            for cat in self.category:
                for words in self.input_words:
                    if words in self.wordLocation[cat].keys():
                        if title in self.wordLocation[cat][words].keys():
                            score *= len(self.wordLocation[cat][words][title])
            self.freqcounts[title] = score
        try:
            freqNormalized = self.normalizescores(self.freqcounts)
            #sorted_norm = sorted(freqNormalized.items(), key=operator.itemgetter(1),reverse = True)
            return freqNormalized
        except: tkMessageBox.showwarning('','No words could be found!\n Try something else!')

    #Its a version of the citation score
    def citScore(self):
        self.citcounts = {}
        for title in self.results:
            self.citcounts[title] = float(self.citationDict[title])
        try:
            citNormalized = self.normalizescores(self.citcounts)
            #sorted_cit = sorted(citNormalized.items(), key=operator.itemgetter(1),reverse = True)
            return citNormalized
        except: tkMessageBox.showwarning('','No words could be found!\n Try something else!')


    #It normalizes our results(copied)
    def normalizescores(self,scores,smallIsBetter=0):  # I might need this one aswell
        vsmall = 0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            minscore=max(minscore, vsmall)
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])


    #Creates the 3 main databases if they are not created before
    def openshelve(self):
        # {url_string : 0}
        self.urlList = shelve.open("urlList.db", flag= 'c')
        # {paperType : {word : {paper_Title : [loc1, loc2, loc3, ...., locN]}}}
        self.wordLocation = shelve.open("wordLocation.db", flag= 'c')
        # {paperType : {paper_Title : 'num of citations'}}
        self.citationDict = shelve.open("citationDict.db", flag='c')

    #Closes the databases
    def close(self):
        self.urlList.close()
        self.wordLocation.close()
        self.citationDict.close()







































def main():



    root = Tk()
    app = Proj5(root)
    app.winfo_geometry()
    root.rowconfigure(0, weight=5)
    root.columnconfigure(0, weight=5)
    root.mainloop()

main()