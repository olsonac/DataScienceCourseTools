import sys
import os
import re
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog,Label,Button,Checkbutton

class DirectoryDiff:
    def __init__(self, master):
        self.master = master
        self.OldDirectoryName = ""
        self.NewDirectoryName = ""

        self.label = Label(master, text="Pick directories to compare")
        self.label.pack()

        self.old_directory_button = Button(master, text="Pick old directory", command=self.GetOldDirectoryName)
        self.old_directory_button.pack()

        self.old_directory_label = Label(master, text="")
        self.old_directory_label.pack()

        self.new_directory_button = Button(master, text="Pick new directory", command=self.GetNewDirectoryName)
        self.component_button.pack()

        self.new_directory_label = Label(master, text="")
        self.new_directory_label.pack()

        self.file_search_string = Entry(master)
        self.file_search_string.pack()

        self.get_differences_button = Button(master, text="Get file differences", command=self.GetDifferences)
        self.get_differences_button.pack()

 def GetOldDirectoryName(self):
    self.OldDirectoryName=filedialog.askdirectory()

 def GetNewDirectoryName(self):
    self.NewDirectoryName=filedialog.askdirectory()

def GetDifferences(self):
    self.old_directory_label['text'] = self.OldDirectoryName
    self.new_directory_label['text'] = self.NewDirectoryName
    search_string = file_search_string.get()
    OldFileList = []
    NewFileList = []
    for (dirpath, dirnames, filenames) in walk(self.OldDirectoryName):
        OldFileList.extend(filenames)
        break
    for (dirpath, dirnames, filenames) in walk(self.NewDirectoryName):
        NewFileList.extend(filenames)
        break
    print("Old files: ",OldFileList)
    print("New files: ",NewFileList)

root = tk.Tk()
DirectoryDiff(root)
root.title("Find file differences in two directories")
root.mainloop()