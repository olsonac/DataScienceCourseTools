import sys
import os
import re
import pandas as pd
import numpy as np
import tkinter as tk
import tkinter.filedialog
from itertools import compress
#from tkinter import filedialog,Label,Button,Checkbutton,Entry

class DirectoryDiff:
    def __init__(self, master):
        self.master = master
        self.OldDirectoryName = ""
        self.NewDirectoryName = ""

        self.label = tk.Label(master, text="Pick directories to compare")
        self.label.pack()

        self.old_directory_button = tk.Button(master, text="Pick old directory", command=self.GetOldDirectoryName)
        self.old_directory_button.pack()

        self.old_directory_label = tk.Label(master, text="")
        self.old_directory_label.pack()

        self.new_directory_button = tk.Button(master, text="Pick new directory", command=self.GetNewDirectoryName)
        self.new_directory_button.pack()

        self.new_directory_label = tk.Label(master, text="")
        self.new_directory_label.pack()

        self.file_search_string = tk.Entry(master)
        self.file_search_string.pack()

        self.get_differences_button = tk.Button(master, text="Get file differences", command=self.GetDifferences)
        self.get_differences_button.pack()

    def GetOldDirectoryName(self):
        self.OldDirectoryName=tk.filedialog.askdirectory()
#        OldDirectoryNameOnly = os.path.split(self.OldDirectoryName)[1]
        self.old_directory_label['text'] = self.OldDirectoryName

    def GetNewDirectoryName(self):
        self.NewDirectoryName=tk.filedialog.askdirectory()
#        NewDirectoryNameOnly = os.path.split(self.NewDirectoryName)[1]
        self.new_directory_label['text'] = self.NewDirectoryName

    def GetDifferences(self):
        search_string = self.file_search_string.get()
        OldFileList = []
        NewFileList = []
        for (dirpath, dirnames, filenames) in os.walk(self.OldDirectoryName):
            OldFileList.extend(filenames)
            break
        for (dirpath, dirnames, filenames) in os.walk(self.NewDirectoryName):
            NewFileList.extend(filenames)
            break
        file_spec = re.compile(search_string)
        MatchingOldFileList = list(filter(file_spec.match, OldFileList))
        MatchingNewFileList = list(filter(file_spec.match, NewFileList))
        print("Old files: ",MatchingOldFileList)
        print("New files: ",MatchingNewFileList)
        print("Search string; ",search_string)

        file_shared=np.zeros(len(MatchingNewFileList))
        FilesNotFound=[]
        for fn in MatchingOldFileList:
            try:
                MatchIndex = MatchingNewFileList.index(fn)
                file_shared[MatchIndex] = 1
            except ValueError:
                print("Didn't find: ", fn)
                FilesNotFound.append(fn)

        NewFiles = list(compress(MatchingNewFileList, (file_shared == 0)))

        LogFilename = self.NewDirectoryName + "/DirectoryDifferences.log"
        LogFile=open(LogFilename, 'w')

        print("Directories compared: ",file=LogFile)
        print("Old: ",self.OldDirectoryName,file=LogFile)
        print("New: ",self.NewDirectoryName,file=LogFile)
        print("\n\nThere were ",len(MatchingOldFileList)," old files: ",file=LogFile)
        for fn in MatchingOldFileList:
            print(fn,file=LogFile)
        print("\n\nThere were ",len(FilesNotFound)," old files not found in the new set: ",file=LogFile)
        for fn in FilesNotFound:
            print(fn,file=LogFile)
        print("\n\nThere were ",len(NewFiles)," new files: ",file=LogFile)
        for fn in NewFiles:
            print(fn,file=LogFile)
        LogFile.close()
        self.master.quit()
        self.master.destroy()

root = tk.Tk()
DirectoryDiff(root)
root.title("Find file differences in two directories")
root.mainloop()