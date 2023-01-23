# sends mark results to students based on autograde.csv
# and plot_marks.csv from the "marking" directory of the component
# make sure to run ExtractMarksFromPlotfile.py first to extract plot marks
# from the plot_nb.ipynb file if there are plot marks to return

import sys

import os
import re
import pandas as pd
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog,Label,Button,Checkbutton

class EmailStudentResults:
    def __init__(self, master):
        self.master = master
        self.AutogradeFilename = ""
        self.PlotmarksFilename = ""
        self.ComponentFilename = ""
        self.CurrentFolder = ""
        self.ComponentDirectory = ""
        self.ComponentName = ""

        # testing or sending?
        self.TestRun = tk.IntVar(value=1) # for testing
        self.HasPlotfile = 0 # is there a plot file to read?

        self.label = Label(master, text="Pick files with information for emailing")
        self.label.pack()

        self.autograde_button = Button(master, text="Click to pick autograde.csv file", command=self.GetAutogradeFilename)
        self.autograde_button.pack()

        self.autograde_label = Label(master, text="")
        self.autograde_label.pack()

        self.hasplotfile_button = Checkbutton(master, text="Is there a plot file (with plot marks)?",\
                                              variable=self.HasPlotfile,onvalue=1)
        self.hasplotfile_button.pack()

        self.plotfile_button = Button(master, text="Click to pick plot_marks.csv file", command=self.GetPlotmarksFilename)
        self.plotfile_button.pack()

        self.plotfile_label= Label(master, text="")
        self.plotfile_label.pack()

        self.component_button = Button(master, text="Click to pick component.csv file", command=self.GetComponentFilename)
        self.component_button.pack()

        self.component_label = Label(master, text="")
        self.component_label.pack()

        self.Concat_button = Button(master, text="Email results", command=self.email_results)
        self.Concat_button.pack()

    # for testing before sending
    def prepare_to_send(self, email_address, subject, contents, attachments, test_dir): # was yagtest_send
        saved_current_dir=os.getcwd()
        if not os.path.isdir(test_dir):
            os.mkdir(test_dir)
        os.chdir(test_dir)
        output_file = open(email_address+".txt", 'w')
        print("To: ",email_address,"\n",file=output_file)
        print("Subject: ",subject,"\n",file=output_file)
        print(contents,file=output_file)
        print("attachments: ",attachments,file=output_file)
        output_file.close()
        os.chdir(saved_current_dir)
        return(1)

    def email_results(self):
        re_for_match=re.compile(".+ipynb$")

        all_notebook_marks = pd.read_csv(self.AutogradeFilename)
        print("HasPlotfile: ",self.HasPlotfile)
        if(self.HasPlotfile):
            all_plot_marks = pd.read_csv(self.PlotmarksFilename)
        all_total_marks = pd.read_csv(self.ComponentFilename)

        all_files = os.listdir(self.ComponentDirectory)
        rmd_files=list(filter(re_for_match.match,all_files))
        for filename in rmd_files:
            print("file: ",filename)
            ID=re.sub("\.ipynb","",filename)
            print("ID: ",ID)
            notebook_marks=all_notebook_marks.loc[all_notebook_marks["SIS Login ID"] == ID]
            notebook_marks=notebook_marks.transpose()
            notebook_marks.rename(columns={0:'-'})
            # print("\nnotebook marks: \n",notebook_marks)
            notebook_total = sum(notebook_marks.iloc[1:-1,0].astype(float))
            # print("notebook total: \n",notebook_total)
            if (self.HasPlotfile):
                plot_marks=all_plot_marks.loc[all_plot_marks["ID"] == ID,all_plot_marks.columns != "ID"]
                plot_marks=plot_marks.transpose()
                plot_marks.rename(columns = {list(plot_marks.columns)[0]:'-'})
                plot_marks=plot_marks.astype(float)
                # print("\nplot marks: \n",plot_marks)
                plot_total = sum(plot_marks.iloc[:,0])
            total_mark=all_total_marks.loc[all_total_marks["SIS Login ID"] == ID,\
                                            all_total_marks.columns == "Mark"].astype(float)
            total_mark=total_mark.iloc[0,0]
            # print("\ntotal mark: ",total_mark,"\n\n")
            contents1 = \
                "Hi,\n Please find your marks for component "+self.ComponentName+" below: \n" + \
                str('\n'.join(notebook_marks.to_string().split('\n')[1:]))
            if (self.HasPlotfile):
                contents2 = "\n\nYour plot marks are: \n" + \
                str('\n'.join(plot_marks.to_string().split('\n')[1:])) + \
               "\n\nManual adjustments to notebook marks [see comments in the notebook] were: \n" + \
                str(total_mark - plot_total - notebook_total) + \
                "\n\nIf you have questions please email Andrew at a.c.olson@bham.ac.uk\nregards,\nAndrew"
            else:
                contents2 = "\n\nManual adjustments to notebook marks [see comments in the notebook] were: \n" + \
                            str(total_mark - notebook_total) + \
                            "\n\nIf you have questions please email Andrew at a.c.olson@bham.ac.uk\nregards,\nAndrew"
            contents = contents1 + contents2
            # print(contents)
            email="acolsonolson@gmail.com" # for testing
            # email=ID+"@bham.ac.uk"
            print("Test value is: ",self.TestRun.get())

            if(self.TestRun.get() == 1):
                # for testing
                print("--TEST--")
                print("email: ",email)
                self.yagsend_test(email_address=email,\
                             subject="Marks for component: "+self.ComponentName,\
                             contents=contents,\
                             attachments=[self.ComponentDirectory+"/"+ID+".ipynb",self.ComponentDirectory+"/"+ID+".Rmd"],\
                             test_dir = self.ComponentDirectory+"/yagmail_test")
                print("Test sending results for ", self.ComponentName, " to ", email)
            else:
                # for sending
                print("--SEND--")
                yag.send(to=email,
                             subject="Marks for component: "+self.ComponentName,\
                             contents=contents,
                             attachments=[self.ComponentDirectory+"/"+ID+".ipynb",self.ComponentDirectory+"/"+ID+".Rmd"])
                print("Sending results for ",self.ComponentName," to ",email)
        print("Done with: ",self.ComponentName)
        self.master.quit()
        self.master.destroy()


    def GetAutogradeFilename(self):
        self.AutogradeFilename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        self.CurrentFolder = os.path.dirname(self.AutogradeFilename)
        os.chdir(self.CurrentFolder)
        os.chdir("..")  # go up one directory to get component directory name
        component_directory = os.getcwd()
        component_name = os.path.basename(os.path.normpath(component_directory))
        filename_only=os.path.split(self.AutogradeFilename)[1]
        self.autograde_label['text']=component_name+"/"+filename_only
        self.CurrentFolder = os.path.dirname(self.AutogradeFilename)
        os.chdir(self.CurrentFolder)

    def GetPlotmarksFilename(self):
        self.PlotmarksFilename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        filename_only = os.path.split(self.PlotmarksFilename)[1]
        self.CurrentFolder = os.path.dirname(self.PlotmarksFilename)
        os.chdir(self.CurrentFolder)
        os.chdir("..")  # go up one directory to get component directory name
        self.ComponentDirectory = os.getcwd()
        print("Component directory: ", self.ComponentDirectory)
        self.ComponentName = os.path.basename(os.path.normpath(self.ComponentDirectory))
        self.plotfile_label['text'] = self.ComponentName + "/" + filename_only
        os.chdir(self.CurrentFolder)


        self.CurrentFolder = os.path.dirname(self.PlotmarksFilename)
        os.chdir(self.CurrentFolder)
        os.chdir("..")  # go up one directory to get component directory name
        self.ComponentDirectory = os.getcwd()
        print("Component directory: ", self.ComponentDirectory)
        self.ComponentName = os.path.basename(os.path.normpath(self.ComponentDirectory))
        filename_only=os.path.split(self.PlotmarksFilename)[1]
        self.autograde_label['text']=component_name+"/"+filename_only
        self.CurrentFolder = os.path.dirname(self.PlotmarksFilename)
        os.chdir(self.CurrentFolder)

    def GetComponentFilename(self):
        self.ComponentFilename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        filename_only = os.path.split(self.ComponentFilename)[1]
        self.CurrentFolder = os.path.dirname(self.ComponentFilename)
        os.chdir(self.CurrentFolder)
        os.chdir("..") # go up one directory to get component directory name
        self.ComponentDirectory = os.getcwd()
        print("Component directory: ",self.ComponentDirectory)
        self.ComponentName =os.path.basename(os.path.normpath(self.ComponentDirectory))
        self.component_label['text'] = self.ComponentName + "/" + filename_only
        os.chdir(self.CurrentFolder)

root = tk.Tk()
yag = yagmail.SMTP('olsonadatascience@gmail.com')
my_concat_wav = EmailStudentResults(root)
root.title("Email student results")
root.mainloop()