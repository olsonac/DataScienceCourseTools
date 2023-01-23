import os
import re
import pandas as pd
import numpy as np
import sys
import zipfile2 as zp
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Label, Button

class unzip_all_to_folders:
    def __init__(self, master):
        self.master = master
        self.zipfile_directory = ""
        self.CurrentFolder = ""

        self.label = Label(master, text="Unzip all .zip files to folders")
        self.label.pack()

        self.directory_button= Button(master, text="Click to pick directory with .zip files.",
                                         command=self.GetZipfilesDirectory)
        self.directory_button.pack()

        self.directory_label = Label(master, text="")
        self.directory_label.pack()

        self.unzip_button = Button(master, text="Unzip all .zip files to folders", command=self.UnzipFiles)
        self.unzip_button.pack()

    def GetZipfilesDirectory(self):
        self.zipfile_directory = fd.askdirectory(title='Choose the directory with marked notebooks')
        print("** directory with .zip files: ", self.zipfile_directory)
        self.directory_label['text'] = self.zipfile_directory
        os.chdir(self.zipfile_directory)
        os.chdir("../..")

    def UnzipFiles(self):
        extension_to_search = "\.zip"
        re_string = ".*"+extension_to_search+"$"
        re_for_files=re.compile(re_string)

        # get list of .Rmd files in marked directory
        all_files_in_directory = os.listdir(self.zipfile_directory)
        marked_files = list(filter(re_for_files.match,all_files_in_directory))
        marked_filename_only=[re.sub(extension_to_search,"",cur_file) for cur_file in marked_files]
        print("marked_filename_only:\n",marked_filename_only)

        os.chdir(self.zipfile_directory)
        for fname in marked_filename_only:
            with zp.ZipFile(fname+".zip", 'r') as zip_ref:
                zip_ref.extractall(fname)

        self.master.quit()
        self.master.destroy()


root = tk.Tk()
unzip_all_to_folders(root)
root.title("Unzip all .zip files to folders")
root.mainloop()
