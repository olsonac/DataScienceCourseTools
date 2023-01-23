import sys

import os
import re
import pandas as pd
import numpy as np
import sys
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Label,Button

class MarkSubmittedNotebooks:
    def __init__(self, master):
        self.master = master
        self.submissions_directory = ""
        self.gradebook_filename = ""
        self.CurrentFolder = ""

        self.label = Label(master, text="Mark submitted notebooks in CANVAS gradebook")
        self.label.pack()

        self.submissions_button = Button(master, text="Click to pick submissions directory", command=self.GetSubmissionsDirectory)
        self.submissions_button.pack()

        self.submissions_label= Label(master, text="")
        self.submissions_label.pack()

        self.gradebook_button = Button(master, text="Click to pick gradebook file", command=self.GetGradebookFilename)
        self.gradebook_button.pack()

        self.gradebook_label= Label(master, text="")
        self.gradebook_label.pack()

        self.mark_button = Button(master, text="Mark submissions in gradebook", command=self.MarkSubmissions)
        self.mark_button.pack()

    def GetSubmissionsDirectory(self):
        self.submissions_directory = fd.askdirectory(title='Choose the submissions directory')
        print("** submissions directory: ", self.submissions_directory)
        self.submissions_label['text'] = self.submissions_directory
        os.chdir(self.submissions_directory)
        os.chdir("..")

    def GetGradebookFilename(self):
        self.gradebook_filename = fd.askopenfilename(initialdir=".", \
                        title="Select file", \
                        filetypes=((".csv files", "*.csv"), ("all files", "*.*")))
        print("** gradebook filename: ", self.gradebook_filename)
        self.gradebook_label['text'] = self.gradebook_filename

    def MarkSubmissions(self):
        re_for_ipynb=re.compile(".*ipynb$")

        # get list of ipynb files submitted to canvas (not ipynb files in marked set of files)
        all_files_ipynb_directory = os.listdir(self.submissions_directory)
        ipynb_files=list(filter(re_for_ipynb.match,all_files_ipynb_directory))
        # print(ipynb_files)
        ipynb_filename_only=[re.sub("\.ipynb","",cur_file) for cur_file in ipynb_files]

        submitted_df = pd.DataFrame(ipynb_filename_only,columns=["filename"])
#        print("submitted_df: \n",submitted_df["filename"])
        submitted_df["ID"]=submitted_df["filename"].str.split("_",3,expand=True)[1] # extract ID code from filename and put in ID column

        potential_ID_for_late_files=submitted_df["filename"].str.split("_",3,expand=True)[2]
        print("submitted_df: ",submitted_df[submitted_df["ID"] == "LATE"])
        print("potential_id_for_late_files: ",potential_ID_for_late_files[submitted_df["ID"] == "LATE"])
        if(len(potential_ID_for_late_files) > 0):
            submitted_df[submitted_df["ID"] == "LATE"] = potential_ID_for_late_files[submitted_df["ID"] == "LATE"]
        # extract ID code from filename and put in ID column
        submitted_df["ID"]=submitted_df["ID"].astype(int)
        submitted_df.set_index("ID",inplace=True,drop=False)

        # print(submitted_df)

        gradebook_df=pd.read_csv(self.gradebook_filename)
        print("gradebook student column: ",gradebook_df["Student"][0:5])
        print(gradebook_df["Student"][0])
        print("Points Possible" in gradebook_df["Student"][0])
        if("Points Possible" in gradebook_df["Student"][0]):
            print("dropping header line with 'Points Possible'")
            gradebook_df=gradebook_df.drop([0])
        print("top of gradebook: \n",gradebook_df.head())
        print("problem lines: \n",gradebook_df[gradebook_df.isin([np.nan, np.inf, -np.inf]).any(1)])
        gradebook_df["ID"]=gradebook_df["ID"].astype(int)
        gradebook_df.set_index("ID",inplace=True,drop=False)
        if("submitted" not in gradebook_df):  # check if column already exists
            gradebook_df["submitted"]=0

        # print(list(submitted_df["ID"]))
        gradebook_df.loc[list(submitted_df["ID"]),"submitted"]=1
        # print(gradebook_df)
        gradebook_wo_extension = os.path.splitext(self.gradebook_filename)
        print("gradebook name w/o extension: ",gradebook_wo_extension)
        gradebook_df.to_csv(gradebook_wo_extension[0] + "_submitted.csv")

        self.master.quit()
        self.master.destroy()

root = tk.Tk()
MarkSubmittedNotebooks(root)
root.title("Mark submitted notebooks in CANVAS gradebook")
root.mainloop()