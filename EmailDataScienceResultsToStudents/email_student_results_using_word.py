# Prepares to send mark results to students based on autograde.csv
# and plot_marks.csv from the "marking" directory of the component
# Make sure to run ExtractMarksFromPlotfile.py first to extract plot marks
# from the plot_nb.ipynb file if there are plot marks to return
#
# This version writes a .csv file that is appropriate for a mail merge using
# ms power automate.  See the description here: https://www.youtube.com/watch?v=Nl5AoLusNR4&t=1074s
# or in documentation for this file

import os
import re
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog,Label,Button,Checkbutton

class EmailStudentResults:
    def __init__(self, master):
        self.master = master
        self.autograde_filename = ""
        self.plot_marks_filename =  ""
        self.component_filename = ""
        self.current_folder = ""
        self.component_directory = ""
        self.component_name = ""
        self.current_folder = ""
        self.number_of_submissions = 0

        # testing or sending?
        self.test_run = tk.IntVar(value=1) # for testing
        # self.has_plot_file = 0 # is there a plot file to read?
        self.has_plot_file = tk.IntVar()

        self.label = Label(master, text="Pick files with information for emailing")
        self.label.pack()

        self.autograde_button = Button(master, text="Click to pick autograde.csv file", command=self.GetAutogradeFilename)
        self.autograde_button.pack()

        self.autograde_label = Label(master, text="")
        self.autograde_label.pack()

        self.hasplotfile_button = Checkbutton(master, text="Is there a plot file (with plot marks)?",\
                                              variable=self.has_plot_file,onvalue=1,offvalue=0)
        self.hasplotfile_button.pack()

        self.plotfile_button = Button(master, text="Click to pick plot_marks.csv file", command=self.GetPlotmarksFilename)
        self.plotfile_button.pack()

        self.plotfile_label= Label(master, text="")
        self.plotfile_label.pack()

        self.component_button = Button(master, text="Click to pick component.csv file", command=self.GetComponentFilename)
        self.component_button.pack()

        self.component_label = Label(master, text="")
        self.component_label.pack()

        self.Concat_button = Button(master, text="Make merge information file", command=self.make_merge_information)
        self.Concat_button.pack()

    def make_merge_information(self):
        # main loop that takes information provided and writes an excel file that can
        # be used with ms power_automate to send results to students

        re_for_match=re.compile(".+ipynb$")

        notebook_marks_df = pd.read_csv(self.autograde_filename)
        notebook_marks_df = notebook_marks_df[notebook_marks_df["SIS Login ID"] != ""]
        self.number_of_submissions = len(notebook_marks_df)
        # print("number of submissions: ",self.number_of_submissions)

        print("HasPlotfile: ",self.has_plot_file)
        if(self.has_plot_file.get()):
            plot_marks_df = pd.read_csv(self.plot_marks_filename)
        total_marks_df = pd.read_csv(self.component_filename)

        all_files = os.listdir(self.component_directory)
        notebook_files=list(filter(re_for_match.match,all_files))
        # print("** notebook files **\n",notebook_files)

        all_files_to_attach=[]
        all_component_names=[]
        all_notebook_marks=[]
        all_plot_marks=[]
        all_manual_adjustments=[]
        all_email_addresses=[]
        for notebook_filename in notebook_files:
            print("\n\n*********\nworking on file: ",notebook_filename)
            all_files_to_attach = np.append(all_files_to_attach,notebook_filename)
            ID=re.sub("\.ipynb","",notebook_filename)
            # print("ID: ",ID)
            notebook_marks=notebook_marks_df.loc[notebook_marks_df["SIS Login ID"] == ID,:]
            notebook_marks=notebook_marks.transpose()
            notebook_marks.rename(columns={0:'-'})
            # print("\nnotebook marks: \n",notebook_marks)
            notebook_total = sum(notebook_marks.iloc[1:-1,0].astype(float))
            # print("notebook total: \n",notebook_total)
            plot_total = 0
            print("has plot file?: ",self.has_plot_file)
            if (self.has_plot_file.get()):
                plot_marks=plot_marks_df.loc[plot_marks_df["ID"] == ID,plot_marks_df.columns != "ID"]
                plot_marks=plot_marks.transpose()
                plot_marks.rename(columns = {list(plot_marks.columns)[0]:'-'})
                plot_marks=plot_marks.astype(float)
                print("\nplot marks: \n",plot_marks)
                plot_total = np.sum(plot_marks.iloc[:,0].astype(float))
                plot_marks = '\n'.join(plot_marks.to_string().split('\n')[1:])
                print("Plot marks: ", plot_marks)
                all_plot_marks = np.append(all_plot_marks, plot_marks)

            total_mark_series=total_marks_df.loc[total_marks_df["SIS Login ID"] == ID,\
                                            total_marks_df.columns == "Mark"].astype(float) # should only match one value
            total_mark = total_mark_series.iloc[0][0]
            # print("\ntotal mark: ",total_mark,"\n\n")
            all_component_names=np.append(all_component_names,self.component_name)
            notebook_marks ='<br>\n'.join(notebook_marks.to_string().split('\n')[1:])
            all_notebook_marks=np.append(all_notebook_marks,notebook_marks)

            manual_adjustments = total_mark - plot_total - notebook_total
            # print("Manual adjustments: ",manual_adjustments)
            all_manual_adjustments = np.append(all_manual_adjustments,str(total_mark - plot_total - notebook_total))

            email=ID+"@bham.ac.uk"
            all_email_addresses = np.append(all_email_addresses,email)
            # print("**** all_email_addresses ****")
            # print(all_email_addresses)
            # print("***********")

            # print("\n\n--Results for student--\n")
            # print("email: "+email+"\n")
            # print("Notebook marks for component: "+self.component_name+"\n")
            # print(notebook_marks)
            # if(self.has_plot_file):
            #     print("\nMarks for plots: \n")
            #     print(plot_marks)
            # print("\nManual adjustments: \n")
            # print(manual_adjustments)
            # print("\nAttachments: ",notebook_filename)

        # put results in a single dataframe that can be written as a .csv file
        # .csv file must be opened, all info made into a table and saved as .xlsx
        # that is the file that power_automate can use
        results_df = pd.DataFrame()
        results_df["email"] = all_email_addresses
        # print("****** email addresses *****\n")
        # print(all_email_addresses)
        # print("************")
        results_df["component"] = all_component_names
        results_df["notebook_marks"] = all_notebook_marks
        # print("number of email addresses: ",len(all_email_addresses))
        if (self.has_plot_file):
            results_df["plot_marks"] = all_plot_marks
        else:
            results_df["plot_marks"] = np.repeat(np.NaN,self.number_of_submissions)
        results_df["manual_adjustments"] = all_manual_adjustments
        results_df["attachments"] = all_files_to_attach

        results_filename = self.component_name + "_results.csv"
        results_df.to_csv(results_filename,index = False)

        # print("Done with: ",self.component_name)
        self.master.quit()
        self.master.destroy()


    def GetAutogradeFilename(self):
        # Ask for the location of the autograde.csv file
        # This should be in [assignment]/components/[component name]/marking

        # os.chdir("~/Documents/current/teach/IntroToDataScience/Homework/Homework1.1_22-23/components/more_arrays/marking")
        self.autograde_filename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        self.current_folder = os.path.dirname(self.autograde_filename)
        os.chdir(self.current_folder)
        os.chdir("..")  # go up one directory to get component directory name
        component_directory = os.getcwd()
        component_name = os.path.basename(os.path.normpath(component_directory))
        filename_only=os.path.split(self.autograde_filename)[1]
        self.autograde_label['text']=component_name+"/"+filename_only
        os.chdir(self.current_folder)

    def GetPlotmarksFilename(self):
        # Ask for location of the plot marks .csv file if it exists for this assignment
        # If no plots are included in the assignment, leave "has plot file" unticked
        # and nothing is required here

        self.plot_marks_filename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        filename_only = os.path.split(self.plot_marks_filename)[1]
        self.current_folder = os.path.dirname(self.plot_marks_filename)
        os.chdir(self.current_folder)
        # all below is for the label
        os.chdir("..")  # go up one directory to get component directory name
        self.component_directory = os.getcwd()
        os.chdir(self.current_folder)
        print("Component directory: ", self.component_directory)
        self.component_name = os.path.basename(os.path.normpath(self.component_directory))
        self.plotfile_label['text'] = self.component_name + "/" + filename_only
        os.chdir(self.current_folder)

    def GetComponentFilename(self): # to identify "component.csv" file
        # Ask for the location of the "component.csv" file which is normally in the same folder as
        # the autograde.csv file

        self.component_filename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".csv files","*.csv"),("all files","*.*")))
        filename_only = os.path.split(self.component_filename)[1]
        self.CurrentFolder = os.path.dirname(self.component_filename)
        os.chdir(self.CurrentFolder)
        os.chdir("..") # go up one directory to get component directory name
        self.component_directory = os.getcwd()
        print("Component directory: ",self.component_directory)
        self.component_name =os.path.basename(os.path.normpath(self.component_directory))
        self.component_label['text'] = self.component_name + "/" + filename_only
        os.chdir(self.current_folder)

root = tk.Tk()
EmailStudentResults(root)
root.title("Email student results")
root.mainloop()