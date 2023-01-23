import os
import pandas as pd
import re

# directory with previously marked work
homework_directory = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/StructuredDataAssignment"
marked_notebooks_directory = homework_directory + "/components/race_policing"
# directory with the gradebook - usually the directory with new work
gradebook_directory = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/StructuredDataAssignment"
gradebook_name = "2022-01-17T1533_Grades-LM_Introduction_to_Data_Scienc_submitted"
# usually a '_submitted' file
gradebook_filename = gradebook_directory + "/" + gradebook_name + ".csv"

re_for_rmd=re.compile(".*Rmd$")

# get list of .Rmd files in marked directory
all_files_notebooks_directory = os.listdir(marked_notebooks_directory)
rmd_files = list(filter(re_for_rmd.match,all_files_notebooks_directory))
rmd_filename_only=[re.sub("\.Rmd","",cur_file) for cur_file in rmd_files]
marked_df = pd.DataFrame(rmd_filename_only,columns=["SIS Login ID"])
print(marked_df)

gradebook_df=pd.read_csv(gradebook_filename)
if(gradebook_df["Student"][1] == "    Points Possible"):
    gradebook_df=gradebook_df.drop([0,1])
gradebook_df["ID"]=gradebook_df["ID"].astype(int)
gradebook_df.set_index("SIS Login ID",inplace=True,drop=False)
if("marked" not in gradebook_df):
    gradebook_df["marked"]=0
# print(list(submitted_df["ID"]))
gradebook_df.loc[list(marked_df["SIS Login ID"]),"marked"]=1
print(gradebook_df[gradebook_df["marked"] == 1])

gradebook_df.to_csv(gradebook_directory + "/" + gradebook_name + "_marked.csv")
