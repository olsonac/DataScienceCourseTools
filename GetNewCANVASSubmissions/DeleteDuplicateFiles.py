import os
import re
import pandas as pd
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Label, Button, Entry
from pathlib import Path
import numpy as np
import sys


class RecordMarkedNotebooks:
    def __init__(self, master):
        self.master = master
        self.new_submissions_directory = ""
        self.unmarked_files_directory = ""
        self.gradebook_filename = ""
        self.CurrentFolder = ""


        self.label = Label(master, text="Remove already marked notebooks from new submissions")
        self.label.pack()

        self.new_submissions_button = Button(master,\
                                        text="Click to pick directory with all new submissions",\
                                        command=self.GetNewSubmissionsDirectory)
        self.new_submissions_button.pack()

        self.new_submissions_label = Label(master, text="")
        self.new_submissions_label.pack()

        self.unmarked_directory_label = Label(master, text="Name the folder that will have unmarked new submissions")
        self.unmarked_directory_label.pack()

        self.unmarked_directory_name = Entry(master, text="", width=40)
        self.unmarked_directory_name.pack()

        self.new_directory_show = Label(master, text="")
        self.new_directory_show.pack()

        self.gradebook_button = Button(master, text="Click to pick gradebook file", command=self.GetGradebookFilename)
        self.gradebook_button.pack()

        self.gradebook_label = Label(master, text="")
        self.gradebook_label.pack()

        self.get_unmarked_button = Button(master, text="Get unmarked notebooks", command=self.GetUnmarkedFiles)
        self.get_unmarked_button.pack()

    def GetNewSubmissionsDirectory(self):
        self.new_submissions_directory = fd.askdirectory(title='Choose the directory with all new submissions')
        print("** new submissions directory: ", self.new_submissions_directory)
        self.new_submissions_label['text'] = self.new_submissions_directory
        os.chdir(self.new_submissions_directory)

    def GetGradebookFilename(self):
        self.gradebook_filename = fd.askopenfilename(initialdir=".",
                                                     title="Select file",
                                                     filetypes=((".csv files", "*.csv"), ("all files", "*.*")))
        print("** gradebook filename: ", self.gradebook_filename)
        self.gradebook_label['text'] = self.gradebook_filename

    def GetUnmarkedFiles(self):
        self.unmarked_files_directory = str(Path(self.new_submissions_directory).parents[0]) + "/" + self.unmarked_directory_name.get()
        print("Directory for unmarked files: ",self.unmarked_files_directory)

        re_for_rmd=re.compile(".*Rmd$")
        re_for_ipynb=re.compile(".*ipynb$")

        # get list of files that have already been marked from the gradebook
        gradebook_df=pd.read_csv(self.gradebook_filename)
        if ("Points Possible" in gradebook_df["Student"][0]):
            print("dropping header line with 'Points Possible'")
            gradebook_df = gradebook_df.drop([0])
        gradebook_df["ID"]=gradebook_df["ID"].astype(int)
        gradebook_df.set_index("ID",inplace=True,drop=False)
        marked_df=gradebook_df[gradebook_df["marked"] == 1]
        marked_ID = list(marked_df["ID"])
        marked_email = list(marked_df["SIS Login ID"])

        os.system('mkdir '+self.unmarked_files_directory)
        # print marked file ID to 'marked_files.txt'
        with open(self.unmarked_files_directory+'/marked_files.txt', 'w') as f:
            [print("  -",curemail,file=f) for curemail in marked_email]

        # print(marked_ID)

        # read file list from the submissions directory, extract the ID number
        # and get the files in the submissions directory that aren't flagged as marked
        # in the gradebook

        # read the list of submitted files (which will include
        # both old and new), put them in a dataframe and index by the ID number
        all_files_new_directory = os.listdir(self.new_submissions_directory)
        new_files = list(filter(re_for_ipynb.match,all_files_new_directory))
        new_files_df = pd.DataFrame(new_files,columns=["filename"])
        # ID_list=[re.sub(".ipynb","",curfile) for curfile in new_rmd_files]
        # print(ID_list)
        new_files_df["ID"]=new_files_df["filename"].str.split("_",4,expand=True)[1]
        potential_ID_for_late_files=new_files_df["filename"].str.split("_",4,expand=True)[2]
        new_files_df.loc[new_files_df["ID"] == "LATE","ID"] = potential_ID_for_late_files[new_files_df["ID"] == "LATE"]
        # extract ID code from filename and put in ID column
        new_files_df["ID"]=new_files_df["ID"].astype(int)
        new_files_df.set_index("ID",inplace=True,drop=False)

        print("\n\nNew submissions: \n")
        print(new_files_df)

        new_files_df["marked"] = 0
        # flag the files that have been marked based on the gradebook entry
        new_files_df.loc[marked_ID,"marked"] = 1

        # put unmarked files in a dataframe
        unmarked_files_df = new_files_df[new_files_df["marked"] == 0]
        print("\n\nNew files to be marked: \n")
        print(unmarked_files_df)
        # put unmarked filenames in a list that we can iterate over to copy to the new_files_only_directory
        unmarked_filenames = list(unmarked_files_df["filename"])
        # print(unmarked_filenames)

        # copy files that haven't been marked to the new_files_only_directory

        [os.system("cp "+self.new_submissions_directory+'/"'+curfile+'" '+self.unmarked_files_directory+'/"'+curfile+'"')\
         for curfile in unmarked_filenames]

        unmarked_gradebook_entries=gradebook_df.loc[(gradebook_df["marked"] == 0) & (gradebook_df['submitted'] == 1)].copy()
        # print(unmarked_gradebook_entries)
        unmarked_gradebook_entries["filename"] = \
            new_files_df.loc[unmarked_gradebook_entries["ID"],"filename"]
        unmarked_file_info_df=unmarked_gradebook_entries[["filename","SIS Login ID","Student","ID"]]
        # print(unmarked_file_info_df)
        unmarked_file_info_df.to_csv(self.unmarked_files_directory+"/"+"file_info.csv")

        new_gradebook=gradebook_df.copy()
        new_gradebook.loc[new_files_df["ID"],"submitted"]=1

        unsubmitted_gradebook_entries=new_gradebook.loc[(new_gradebook['submitted'] == 0)]
        print(unsubmitted_gradebook_entries)
        unsubmitted_file_info_df=unsubmitted_gradebook_entries[["SIS Login ID","Student","ID"]]
        print(unsubmitted_file_info_df)
        unsubmitted_file_info_df.to_csv(self.unmarked_files_directory+"/"+"unsubmitted_file_info.csv")

        self.master.quit()
        self.master.destroy()


root = tk.Tk()
RecordMarkedNotebooks(root)
root.title("Get unmarked notebooks and put in a separate directory")
root.mainloop()