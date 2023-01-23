import os
import re
import pandas as pd
import numpy as np
import sys
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Label, Button

class RecordMarkedNotebooks:
    def __init__(self, master):
        self.master = master
        self.components_directory = ""
        self.gradebook_filename = ""
        self.CurrentFolder = ""

        self.label = Label(master, text="Record marked notebooks in CANVAS gradebook")
        self.label.pack()

        self.components_button = Button(master, text="Click to pick directory with marked notebooks (usually components/[homework_name])",
                                         command=self.GetComponentsDirectory)
        self.components_button.pack()

        self.components_label = Label(master, text="")
        self.components_label.pack()

        self.gradebook_button = Button(master, text="Click to pick gradebook file", command=self.GetGradebookFilename)
        self.gradebook_button.pack()

        self.gradebook_label = Label(master, text="")
        self.gradebook_label.pack()

        self.mark_button = Button(master, text="Record marked homework in gradebook", command=self.RecordMarkedFiles)
        self.mark_button.pack()

    def GetComponentsDirectory(self):
        self.components_directory = fd.askdirectory(title='Choose the directory with marked notebooks')
        print("** components directory: ", self.components_directory)
        self.components_label['text'] = self.components_directory
        os.chdir(self.components_directory)
        os.chdir("../..")

    def GetGradebookFilename(self):
        self.gradebook_filename = fd.askopenfilename(initialdir=".", \
                                                     title="Select file", \
                                                     filetypes=((".csv files", "*.csv"), ("all files", "*.*")))
        print("** gradebook filename: ", self.gradebook_filename)
        self.gradebook_label['text'] = self.gradebook_filename

    def RecordMarkedFiles(self):
        extension_to_search = "\.Rmd"
        re_string = ".*"+extension_to_search+"$"
        re_for_files=re.compile(re_string)

        # get list of .Rmd files in marked directory
        all_files_notebooks_directory = os.listdir(self.components_directory)
        marked_files = list(filter(re_for_files.match,all_files_notebooks_directory))
        marked_filename_only=[re.sub(extension_to_search,"",cur_file) for cur_file in marked_files]
        print("marked_filename_only:\n",marked_filename_only)
        marked_df = pd.DataFrame(marked_filename_only,columns=["SIS Login ID"])
        print(marked_df)

        gradebook_df=pd.read_csv(self.gradebook_filename)
        if ("Points Possible" in gradebook_df["Student"][0]):
            print("dropping header line with 'Points Possible'")
            gradebook_df = gradebook_df.drop([0])
        gradebook_df["ID"]=gradebook_df["ID"].astype(int)
        gradebook_df.set_index("SIS Login ID",inplace=True,drop=False)
        if("marked" not in gradebook_df):
            gradebook_df["marked"]=0
        # print(list(submitted_df["ID"]))
        gradebook_df.loc[list(marked_df["SIS Login ID"]),"marked"]=1
        print(gradebook_df[gradebook_df["marked"] == 1])

        gradebook_wo_extension = os.path.splitext(self.gradebook_filename)
        print("gradebook name w/o extension: ",gradebook_wo_extension)
        gradebook_df.to_csv(gradebook_wo_extension[0] + "_marked.csv")

        self.master.quit()
        self.master.destroy()

root = tk.Tk()
RecordMarkedNotebooks(root)
root.title("Record marked notebooks in CANVAS gradebook")
root.mainloop()
