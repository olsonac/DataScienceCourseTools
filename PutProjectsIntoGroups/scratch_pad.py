import os
import numpy as np
import pandas as pd
import re
import difflib as df
import shutil

os.chdir("/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/projects2022-23/submissions")
start_path="/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/projects2022-23/submissions"

def get_ipynb_contents(start_path,content_length):
    dir_array = []
    file_array = []
    for root, dirs, dir_files in os.walk(start_path):
        print("\nroot: ",root,"\n")
        print(" dir: ",dirs,"\n")
        for cur_file in dir_files:
           dir_array.append(root)
           file_array.append(cur_file)

    files_to_search = pd.DataFrame()
    files_to_search["directory"] = dir_array
    files_to_search["file"] = file_array

    # remove "I/init notebook.ipynb"
    files_to_search = files_to_search[~(files_to_search.file.str.contains("[iI]nit notebook"))]
    # remove .[something] files which can be .[something]ipynb
    dot_file_marker = pd.Series((files_to_search.file.str.match(r"\.",na=True)))
    files_to_search = files_to_search[~(dot_file_marker.values)]

    # print("\n***** after dot files removed******")
    # print(files_to_search.to_string())

    # remove READ ME files which can be READ ME.ipynb
    ipynb_list=files_to_search[~(files_to_search.file.str.contains(r"READ *ME",na=True))].copy()

    # print("\n*** inpynb list - READ ME removed  ***")
    # print(ipynb_list.to_string())

    # get only .ipynb (jupyter notebook) files
    ipynb_list=ipynb_list[(ipynb_list.file.str.contains(r".ipynb$",na=False))].copy()
    ipynb_list.reset_index(drop=True, inplace=True)

    print("\n*** inpynb list - only ipynb ***")
    print(ipynb_list.to_string())

    print(ipynb_list.iloc[0,0])
    print(ipynb_list.iloc[0,1])
    content_list=[]
    for i, cur_file_name in enumerate(ipynb_list["file"]):
        file_path = ipynb_list.iloc[i]["directory"]+"/"+cur_file_name
        print(file_path,":")
        current_file = open(file_path)
        content_beginning = current_file.read(content_length)
        print(content_beginning)
        content_list.append(content_beginning)
    ipynb_list["contents"] = content_list
    return(ipynb_list)

def GroupFolders():
    content_length=1000
    start_path = os.getcwd()
    ipynb_list = get_ipynb_contents(start_path,content_length)

    num_ipynb = np.unique(ipynb_list["directory"],return_counts = True)
    # need to add check for directories with no .ipynb files after removals
    # this happens, for example, if the project is called README.ipynb
    problem_directories = num_ipynb[1] > 1
    if np.count_nonzero(problem_directories) > 0:
        problem_names = num_ipynb[0][problem_directories]
        print("These directories have more than one potential project (.ipynb files that are not init)")
        print("Fix and run again")
        print(problem_names)
        # fix in future by selecting the largest single .ipynb file to compare or by averaging
        exit()

    list_length = len(ipynb_list)
    all_ratios = np.zeros(list_length * list_length)
    all_ratios = all_ratios.reshape(list_length,list_length)
    directory_log = [] # for log file that lists which student directories are in which groups
    group_number_log = []
    group_subnumber_log = []
    for i in np.arange(list_length):
        for j in np.arange(list_length):
            current_ratio = df.SequenceMatcher(None,ipynb_list["contents"][i],
                                               ipynb_list["contents"][j]).quick_ratio()
            all_ratios[i][j] = current_ratio

    similarity_threshold = 0.95
    group_counter = 1
    while(len(ipynb_list) > 0):
        current_group = all_ratios[0] > similarity_threshold
        selected_group = ipynb_list.loc[current_group,:].copy()
        selected_group.reset_index(drop=True, inplace=True)
        # print(selected_group["file"])
        group_dir = start_path + "/Group_" + str(group_counter)
        if (not os.path.exists(group_dir)):
            print("making directory: ",group_dir)
            os.mkdir(group_dir)
        for i,current_directory in enumerate(selected_group["directory"]):
            directory_log.append(current_directory)
            group_number_log.append(group_counter)
            group_subnumber_log.append(i)
            group_subdir = group_dir + "/" + "Group_" + str(group_counter) + "_" + str(i)
            print("moving: ", current_directory,"\n    to: ", group_subdir)
            shutil.move(current_directory, group_subdir)

        # take current group entries out of ipynb_list
        not_selected_group = ~(current_group)
        ipynb_list = ipynb_list.loc[not_selected_group,:].copy()
        ipynb_list.reset_index(drop=True, inplace=True)
        all_ratios = all_ratios[not_selected_group] # take out rows
        all_ratios = all_ratios[:,not_selected_group] # take out columns
        group_counter = group_counter + 1
    group_log_information = pd.DataFrame()
    group_log_information["Group"]=group_number_log
    group_log_information["Subdirectory"] = group_subnumber_log
    group_log_information["Directory"]=directory_log
    group_log_information.to_csv("group_log.csv")

GroupFolders()