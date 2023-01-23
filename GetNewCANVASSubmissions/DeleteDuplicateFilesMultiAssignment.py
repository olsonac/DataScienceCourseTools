import os
import pandas as pd
import re

home_directory = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework"
homework_directory_new = "/StructuredDataAssignment2"

submissions_directory = "/submissions"
submissions_directory_new = home_directory + homework_directory_new + submissions_directory

gradebook_directory = home_directory + homework_directory_new
gradebook_name = "2022-01-17T1533_Grades-LM_Introduction_to_Data_Scienc_submitted"
gradebook_filename = gradebook_directory + "/" + gradebook_name + ".csv"

new_files_only_directory = home_directory + homework_directory_new + "/new_submissions"

re_for_zip=re.compile(".*zip$")

# get list of files that have already been marked from the gradebook
gradebook_df=pd.read_csv(gradebook_filename)
if(gradebook_df["Student"][1] == "    Points Possible"):
    gradebook_df=gradebook_df.drop([0,1])
gradebook_df["ID"]=gradebook_df["ID"].astype(int)
gradebook_df.set_index("ID",inplace=True,drop=False)
submitted_df=gradebook_df[gradebook_df["submitted"] == 1]
submitted_ID = list(submitted_df["ID"])
marked_email = list(submitted_df["SIS Login ID"])

os.system('mkdir '+new_files_only_directory)
# print marked file ID to
with open(new_files_only_directory+'/marked_files.txt', 'w') as f:
    [print("  -",curemail,file=f) for curemail in marked_email]

# print(submitted_ID)

# read file list from the submissions directory, extract the ID number
# and get the files in the submissions directory that aren't flagged as marked
# in the gradebook

# read the list of submitted files (which will include
# both old and new), put them in a dataframe and index by the ID number
all_files_new_directory = os.listdir(submissions_directory_new)
new_zip_files = list(filter(re_for_zip.match,all_files_new_directory))
new_files_df = pd.DataFrame(new_zip_files,columns=["filename"])
# ID_list=[re.sub(".ipynb","",curfile) for curfile in new_rmd_files]
# print(ID_list)
ID=new_files_df["filename"].str.split("_",3,expand=True)[1]
ID_nums_for_late=new_files_df["filename"].str.split("_",3,expand=True)[2]

ID_late = ID == "LATE"
ID[ID_late] = ID_nums_for_late[ID_late]
print(ID)
# extract ID code from filename and put in ID column
new_files_df["ID"]=ID.astype(int)
new_files_df.set_index("ID",inplace=True,drop=False)
print(new_files_df)

new_files_df["submitted"] = 0
# flag the files that have been marked based on the gradebook entry
new_files_df.loc[submitted_ID,"submitted"] = 1

# put unmarked files in a dataframe
unmarked_files_df = new_files_df[new_files_df["submitted"] == 0]
# print(unmarked_files_df)
# put unmarked filenames in a list that we can iterate over to copy to the new_files_only_directory
unmarked_filenames = list(unmarked_files_df["filename"])
# print(unmarked_filenames)

# copy files that haven't been marked to the new_files_only_directory

[os.system("cp "+submissions_directory_new+'/"'+curfile+'" '+new_files_only_directory+'/"'+curfile+'"') \
 for curfile in unmarked_filenames]

unmarked_gradebook_entries=gradebook_df.loc[(gradebook_df["submitted"] == 0) )].copy()
# print(unmarked_gradebook_entries)
unmarked_gradebook_entries["filename"] = \
    new_files_df.loc[unmarked_gradebook_entries["ID"],"filename"]
unmarked_file_info_df=unmarked_gradebook_entries[["filename","SIS Login ID","Student","ID"]]
# print(unmarked_file_info_df)
unmarked_file_info_df.to_csv(new_files_only_directory+"/"+"file_info.csv")

new_gradebook=gradebook_df.copy()
new_gradebook.loc[new_files_df["ID"],"submitted"]=1

unsubmitted_gradebook_entries=new_gradebook.loc[(new_gradebook['submitted'] == 0)]
print(unsubmitted_gradebook_entries)
unsubmitted_file_info_df=unsubmitted_gradebook_entries[["SIS Login ID","Student","ID"]]
print(unsubmitted_file_info_df)
unsubmitted_file_info_df.to_csv(new_files_only_directory+"/"+"unsubmitted_file_info.csv")