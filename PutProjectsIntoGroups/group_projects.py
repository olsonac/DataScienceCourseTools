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

def dir_is_same(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
   """

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0:
        return False
    # if len(dirs_cmp.common_files) > 0:
    #     (_, mismatch, errors) = filecmp.cmpfiles(
    #         dir1, dir2, dirs_cmp.common_files, shallow=False)
    #     if len(mismatch) > 0 or len(errors) > 0:
    #         return False
    # for common_dir in dirs_cmp.common_dirs:
    #     new_dir1 = os.path.join(dir1, common_dir)
    #     new_dir2 = os.path.join(dir2, common_dir)
    #     if not dir_is_same(new_dir1, new_dir2):
    #         return False
    else:
        return True

# class dircmp(filecmp.dircmp):
#     """
#     Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
#     subclass compares the content of files with the same path.
#     """
#     def phase3(self):
#         """
#         Find out differences between common files.
#         Ensure we are using content comparison with shallow=False.
#         """
#         fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,
#                                  shallow=False)
#         self.same_files, self.diff_files, self.funny_files = fcomp

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

    def GroupFolders(self):
        all_entries = np.array(os.listdir(self.projects_directory))
        print("Potential directories: \n",all_entries)
        entry_is_dir = np.zeros(len(all_entries))
        for i, entry in enumerate(all_entries):
            entry_is_dir[i] = os.path.isdir(entry)
        dir_boolean = entry_is_dir == 1
        print("Potential directories boolean: \n",dir_boolean)
        dir_entries = all_entries[dir_boolean]
        all_groups = []
        while len(dir_entries) > 0:
            current_proj = dir_entries[0]
            current_group = np.array([current_proj])
            index_of_items_to_delete=np.array([0])
            for i in np.arange(1,len(dir_entries)):
                print("Current proj: ",current_proj)
                print("current dir: ",dir_entries[i])
                dir_same_test = dir_is_same(current_proj,dir_entries[i])
                if(dir_same_test):
                    current_group = np.append(current_group,dir_entries[i])
                    index_of_items_to_delete = np.append(index_of_items_to_delete,i)
            print("Current group: ",current_group)
            print("Indicies to delete: ",index_of_items_to_delete)
            print("dir_entries: ",dir_entries)
            all_groups.append(current_group)
            dir_entries = np.delete(dir_entries,index_of_items_to_delete)

        all_projects = []
        all_group_numbers = []
        for i,current_group in enumerate(all_groups):
            print("Group ",i,": ",current_group)
            print("   \n")
            for j,current_file in enumerate(all_groups[i]):
                cur_dir=os.getcwd()
                group_dir = cur_dir+"/Group_"+str(i)
                current_file_path = cur_dir+"/"+current_file
                new_file_path = group_dir+"/"+current_file
                if(not os.path.exists(group_dir)):
                    os.mkdir(group_dir)
                print("moving ",current_file," to ",new_file_path)
                shutil.move(current_file_path,new_file_path)
                all_projects.append(current_file)
                all_group_numbers.append(i)
        projects_df = pd.DataFrame()
        projects_df["project_file"] = all_projects
        projects_df["group_number"] = all_group_numbers
        projects_df.to_csv("project_and_group_information.csv")
        self.master.quit()
        self.master.destroy()

root = tk.Tk()
group_projects(root)
root.title("Unzip all .zip files to folders")
root.mainloop()
