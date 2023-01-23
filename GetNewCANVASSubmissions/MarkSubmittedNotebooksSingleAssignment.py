import os
import pandas as pd
import re

# /Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/Homework2/submissions
homework_directory = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/Homework2c"
submissions_directory = homework_directory + "/submissions"
gradebook_name = "2022-01-10T0954_Grades-LM_Introduction_to_Data_Scienc"
gradebook_filename = homework_directory + "/" + gradebook_name + ".csv"
re_for_ipynb=re.compile(".*ipynb$")

# get list of ipynb files submitted to canvas (not ipynb files in marked set of files)
all_files_ipynb_directory = os.listdir(submissions_directory)
ipynb_files=list(filter(re_for_ipynb.match,all_files_ipynb_directory))
# print(ipynb_files)
ipynb_filename_only=[re.sub("\.ipynb","",cur_file) for cur_file in ipynb_files]
submitted_df = pd.DataFrame(ipynb_filename_only,columns=["filename"])
submitted_df["ID"]=submitted_df["filename"].str.split("_",3,expand=True)[1] # extract ID code from filename and put in ID column
submitted_df["ID"]=submitted_df["ID"].astype(int)
# print(submitted_df)

gradebook_df=pd.read_csv(gradebook_filename)
if(gradebook_df["Student"][1] == "    Points Possible"):
    gradebook_df=gradebook_df.drop([0,1])
gradebook_df["ID"]=gradebook_df["ID"].astype(int)
gradebook_df.set_index("ID",inplace=True,drop=False)
gradebook_df["submitted"]=0
# print(list(submitted_df["ID"]))
gradebook_df.loc[list(submitted_df["ID"]),"submitted"]=1
# print(gradebook_df)
gradebook_df.to_csv(homework_directory + "/" + gradebook_name + "_submitted.csv")