import sys
import os
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.scrolledtext as st
from itertools import compress
import pandas as pd
import re

class JoinMarksToCANVASGradebook:
    def __init__(self, master):
        self.master = master
        self.assignment_directory = None
        self.marked_results_filename = 'final.csv'
        self.marked_results_df = None
        self.gradebook_assignment_column_name = None
        self.gradebook_df = pd.DataFrame()
        self.number_of_gradebook_header_lines = 1
        self.header_df = pd.DataFrame()
        self.gradebook_filename = None
        self.component_name = "Total"
        self.component_point_value = None

# the % that this assignment is worth (not the number of points/questions in the assignment)
# this script takes the % correct from 'final.csv' and multiplies that by the % the assignment is worth
# The % from the whole course is what CANVAS is expecting

        self.label = tk.Label(master, text="Join marks to CANVAS gradebook").grid(row=0)

        self.gradebook_button = tk.Button(master, text="Click to set the gradebook .csv file",
                                              command=self.PickGradebookFile).grid(row=1)

        self.gradebook_column_display = st.ScrolledText(master,
                            width = 50,
                            height = 8)
        self.gradebook_column_display.grid(row=2)

        self.column_number_info = tk.Label(master,text="Enter the column number for the assignment from the gradebook:").grid(row=3)
        self.column_number_label = tk.Label(master,text="gradebook column number").grid(row=4)
        self.column_number_string = tk.StringVar()
        self.assignment_column_entry = tk.Entry(master,textvariable = self.column_number_string).grid(row=5)

        self.results_button = tk.Button(master, text="Click to set the marked results\n .csv file (usually'final.csv')",
                                        command=self.PickResultsFile).grid(row=6)

        self.results_column_display = st.ScrolledText(master,
                                                        width=50,
                                                        height=4)
        self.results_column_display.grid(row=7)

        self.rcolumn_number_info = tk.Label(master,
                                           text="Enter the column number to get results from (column with % for this assignment, not overall):").grid(
            row=8)
        self.rcolumn_number_label = tk.Label(master, text="results column number").grid(row=9)
        self.rcolumn_number_string = tk.StringVar()
        self.results_column_entry = tk.Entry(master, textvariable=self.rcolumn_number_string).grid(row=10)

        self.percentage_value_string = tk.StringVar()
        self.percentage_info = tk.Label(master,text = "Set this assignment's overall percentage value in the course:").grid(row=11)
        self.percentage_label = tk.Label(master,text = "Percent").grid(row=12)
        self.percentage_value_entry = tk.Entry(master,textvariable = self.percentage_value_string).grid(row=13)

        self.compare_button = tk.Button(master, text="Join marks to CANVAS gradebook",
                                        command=self.JoinMarks).grid(row=14)

    def PickGradebookFile(self):
        self.gradebook_filename = fd.askopenfilenames(title='Choose the gradebook .csv file')
        self.gradebook_filename = self.gradebook_filename[0]
        print("** gradebook file: ", self.gradebook_filename)
        self.gradebook_df = pd.read_csv(self.gradebook_filename)
        self.header_df = self.gradebook_df.head(self.number_of_gradebook_header_lines)
        print("header for gradebook_data_df: \n", self.header_df)
        gradebook_column_names = self.gradebook_df.columns
        print("column names for gradebook_data_df:\n")
        column_name_text=""
        for i, column_name in enumerate(gradebook_column_names):
            column_name_text = column_name_text + str(i) + ": " + column_name + "\n"
        self.gradebook_column_display.insert(tk.INSERT,column_name_text)
        self.gradebook_column_display.configure(state='disabled')
        self.assignment_directory = os.path.dirname(self.gradebook_filename)
        print("Assignment directory is: ",self.assignment_directory)

    def PickResultsFile(self):
        self.marked_results_filename = fd.askopenfilenames(title='Choose the results .csv file')
        self.marked_results_filename = self.marked_results_filename[0]
        print("** results file: ", self.marked_results_filename)
        self.marked_results_df = pd.read_csv(self.marked_results_filename)
        marked_results_column_names = self.marked_results_df.columns
        print("column names for marked results file:\n")
        column_name_text = ""
        for i, column_name in enumerate(marked_results_column_names):
            column_name_text = column_name_text + str(i) + ": " + column_name + "\n"
        self.results_column_display.insert(tk.INSERT, column_name_text)
        self.results_column_display.configure(state='disabled')
        self.marked_results_df.set_index("SIS Login ID", drop=False, inplace=True)

    def JoinMarks(self):
        self.component_percentage_value = int(self.percentage_value_string.get())
        print("Component percentage value: ",self.component_percentage_value)
        gradebook_assignment_column_number = int(self.column_number_string.get())
        print("Gradebook column number choosen: ",gradebook_assignment_column_number)
        gradebook_assignment_column_name = self.gradebook_df.columns[gradebook_assignment_column_number]
        print("Gradebook column name: ",gradebook_assignment_column_name)
        print("Column: \n",self.gradebook_df[gradebook_assignment_column_name] )

        results_column_number = int(self.rcolumn_number_string.get())
        print("Results column number choosen: ",results_column_number)
        results_column_name = self.marked_results_df.columns[results_column_number]
        print("Results column name: ",results_column_name)
        print("Results values: \n",self.marked_results_df[results_column_name])

        gradebook_data_df = self.gradebook_df.iloc[1:,:].copy()
        gradebook_data_df.set_index("SIS Login ID", drop=False, inplace=True)
        print("gradebook_data_df:\n", gradebook_data_df.iloc[0:5,3:7])


        gradebook_data_df.loc[self.marked_results_df["SIS Login ID"], \
                              gradebook_assignment_column_name] = self.marked_results_df[results_column_name]/100 * \
                                                                  self.component_percentage_value

        print("Merged values: \n",gradebook_data_df.iloc[0:5,gradebook_assignment_column_number])

        gradebook_prefix = re.sub("\.csv", "", self.gradebook_filename)
        self.gradebook_df.to_csv(gradebook_prefix + "(old).csv",
                            index=False)  # save previous gradebook as "old"

        print("changed filename: ",self.gradebook_filename)
        print(self.header_df.iloc[0:5,0:7])
        print("******")
        print(gradebook_data_df.iloc[0:5,0:7])
        self.header_df.to_csv(self.gradebook_filename, index=False)
        gradebook_data_df.to_csv(self.gradebook_filename,
                                 mode="a", index=False, header=False)
        self.master.quit()
        self.master.destroy()



root = tk.Tk()
JoinMarksToCANVASGradebook(root)
root.title("Join marks to exported CANVAS gradebook")
root.mainloop()

