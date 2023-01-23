import sys
import os
import re
import pandas as pd
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd
from itertools import compress

class IdentifyGradebookIDwoHomework:
    def __init__(self, master):
        self.master = master
        self.gradebook_file = None
        self.ID_column_name = "SIS Login ID"
        self.submissions_foler = None
        self.output_df = pd.DataFrame()

        self.label = tk.Label(master, text="Compare CANVAS gradebook ID and submissions")
        self.label.pack()

        self.gradebook_button = tk.Button(master, text="What is the gradebook .csv file?",
                                              command=self.PickGradebookFile)
        self.gradebook_button.pack()

        self.submissions_button = tk.Button(master, text="Where is the notebooks folder?",
                                              command=self.GetSubmissionsFolder)
        self.submissions_button.pack()

        self.compare_button = tk.Button(master, text="Compare gradebook IDs and submission folders.",
                                        command=self.CompareGradebookAndSubmissions)
        self.compare_button.pack()

    def PickGradebookFile(self):
        self.gradebook_file=fd.askopenfilenames(title='Choose the gradebook .csv file')
        self.gradebook_file = self.gradebook_file[0]
        print("** gradebook file: ",self.gradebook_file)

    def GetSubmissionsFolder(self):
        self.submissions_folder = fd.askdirectory()
        print("** done picking submissions folder: ",self.submissions_folder)

    def CompareGradebookAndSubmissions(self):

        print("Reading gradebook file: ", self.gradebook_file)
        gradebook_df=pd.read_csv(self.gradebook_file)
        gradebook_IDs = np.array(gradebook_df[self.ID_column_name].copy())
        gradebook_IDs = gradebook_IDs[gradebook_IDs == gradebook_IDs] # gets rid of nan (nan is not equal to nan - strangely)
        print("Gradebook IDs: ",gradebook_IDs)

        print("Submissions folder: ")
        print(self.submissions_folder)
        assignment_subfolders = [f.name for f in os.scandir(self.submissions_folder) if f.is_dir()]
        assignment_subfolders = np.array(assignment_subfolders)
        print("assignment subfolders: ",assignment_subfolders)

        gradebook_path = os.path.dirname(self.gradebook_file)
        missing_fn = gradebook_path + "/missing_submission_names.txt"
        missing_file=open(missing_fn,"w")

        print("Missing items: \n")
        missing_indicies = np.isin(gradebook_IDs,assignment_subfolders,invert=True)
        missing_IDs = gradebook_IDs[missing_indicies]
        print("missing IDs: ",missing_IDs)
        for ID in missing_IDs:
            missing_file_line="  - "+ID+"\n"
            missing_file.write(missing_file_line)
            print("  - ",ID)

        missing_file.close()
        self.master.quit()
        self.master.destroy()

root = tk.Tk()
IdentifyGradebookIDwoHomework(root)
root.title("Compare gradebook and submissions to identify missing submissions.")
root.mainloop()