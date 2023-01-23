import os
import re
import pandas as pd
import numpy as np
import shutil
import sys
import filecmp
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Label, Button


class group_projects:
    def __init__(self, master):
        self.master = master
        self.projects_directory = ""

        self.label = Label(master, text="group identical project folders")
        self.label.pack()

        self.directory_button= Button(master, text="Click to pick directory with project folders.",
                                         command=self.GetDirectory)
        self.directory_button.pack()

        self.directory_label = Label(master, text="")
        self.directory_label.pack()

        self.group_folders_button = Button(master, text="Group identical project folders", command=self.GroupFolders)
        self.group_folders_button.pack()

    def GetDirectory(self):
        self.projects_directory = fd.askdirectory(initialdir="/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/projects2022-23",
                                                  title='Choose the directory with project folders')
        print("** directory with project folders: ", self.projects_directory)
        self.directory_label['text'] = self.projects_directory
        os.chdir(self.projects_directory)


root = tk.Tk()
group_projects(root)
root.title("Unzip all .zip files to folders")
root.mainloop()
