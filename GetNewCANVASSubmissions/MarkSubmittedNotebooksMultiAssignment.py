import os
import pandas as pd
import re

# /Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/Homework2/submissions
homework_directory = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/StructuredDataAssignment"
submissions_directory = homework_directory + "/submissions2"
gradebook_name = "2022-02-24T1809_Grades-LM_Introduction_to_Data_Scienc"
gradebook_filename = homework_directory + "/" + gradebook_name + ".csv"
re_for_ipynb=re.compile("^[a-z][a-z][a-z][0-9]*$")

os.chdir(submissions_directory)
ID_directories=next(os.walk(submissions_directory))[1]

print("IDs: ",ID_directories)

gradebook_df=pd.read_csv(gradebook_filename)
if(gradebook_df["Student"][1] == "    Points Possible"):
    gradebook_df=gradebook_df.drop([0,1])
gradebook_df.set_index("SIS Login ID",inplace=True,drop=False)
gradebook_df["submitted"]=0
gradebook_df.loc[ID_directories,"submitted"]=1
print(gradebook_df)
gradebook_df.to_csv(homework_directory + "/" + gradebook_name + "_submitted.csv")

# # put people listed in the gradebook who have not submitted into a file
# # for use with assign_config.yaml
#
unsubmitted_df=gradebook_df[gradebook_df["submitted"] == 0]
unsubmitted_ID = list(unsubmitted_df["SIS Login ID"])
print("no submission: \n",unsubmitted_ID)
print("number of people with no submission: ",len(unsubmitted_ID))
#
# # this file can be copied and pasted into assign_config.yaml to ignore entries
# # from the gradebook where no work has been submitted (yet)
with open(homework_directory+'/no_submission_IDs.txt', 'w') as outputfile:
    [print("  -",curID,file=outputfile) for curID in unsubmitted_ID]