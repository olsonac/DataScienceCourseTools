# sends mark results to students based on autograde.csv
# and plot_marks.csv from the "marking" directory of the component
# make sure to run ExtractMarksFromPlotfile.py first to extract plot marks
# from the plot_nb.ipynb file

import sys

import yagmail
import os
import re
import pandas as pd
import numpy as np
import sys

# testing or sending?
# test = 1 # for testing
test = 0 # for sending

# for testing before sending
def yagsend_test(to, subject, contents, attachments, test_dir):
    saved_current_dir=os.getcwd()
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    os.chdir(test_dir)
    output_file = open(to+".txt", 'w')
    print("To: ",to,"\n",file=output_file)
    print("Subject: ",subject,"\n",file=output_file)
    print(contents,file=output_file)
    print("attachments: ",attachments,file=output_file)
    output_file.close()
    os.chdir(saved_current_dir)
    return(1)


home_dir = "/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/Homework2c"
component_dir = home_dir + "/components/race_policing"

re_for_match=re.compile(".+Rmd$")
os.chdir(component_dir)

all_notebook_marks = pd.read_csv("./marking/autograde.csv")
all_plot_marks = pd.read_csv("./marking/plot_marks.csv")
all_total_marks = pd.read_csv("./marking/component.csv")

all_files = os.listdir(component_dir)
rmd_files=list(filter(re_for_match.match,all_files))
for filename in rmd_files:
    # print("file: ",filename)
    ID=re.sub("\.Rmd","",filename)
    notebook_marks=all_notebook_marks.loc[all_notebook_marks["SIS Login ID"] == ID]
    notebook_marks=notebook_marks.transpose()
    notebook_marks.rename(columns={0:'-'})
    # print("\nnotebook marks: \n",notebook_marks)
    notebook_total = sum(notebook_marks.iloc[1:-1,0].astype(float))
    # print("notebook total: \n",notebook_total)
    plot_marks=all_plot_marks.loc[all_plot_marks["ID"] == ID,all_plot_marks.columns != "ID"]
    plot_marks=plot_marks.transpose()
    plot_marks.rename(columns = {list(plot_marks.columns)[0]:'-'})
    plot_marks=plot_marks.astype(float)
    # print("\nplot marks: \n",plot_marks)
    plot_total = sum(plot_marks.iloc[:,0])
    total_mark=all_total_marks.loc[all_total_marks["SIS Login ID"] == ID,\
                                    all_total_marks.columns == "Mark"].astype(float)
    total_mark=total_mark.iloc[0,0]
    # print("\ntotal mark: ",total_mark,"\n\n")
    contents = \
        "Hi,\n Please find your marks for homework 2 below: \n" + \
        str('\n'.join(notebook_marks.to_string().split('\n')[1:])) + \
        "\n\nYour plot marks are: \n" + \
        str('\n'.join(plot_marks.to_string().split('\n')[1:])) + \
        "\n\nManual adjustments to notebook marks [see comments in the notebook] were: \n" + \
        str(total_mark - plot_total - notebook_total) + \
        "\n\nIf you have questions please email Andrew at a.c.olson@bham.ac.uk\nregards,\nAndrew"
    # print(contents)
    # email="olsonac@bham.ac.uk" # for testing
    email=ID+"@bham.ac.uk"

    if(test == 1):
        # for testing
        yagsend_test(to=email,
                     subject="Homework 2 marks",
                     contents=contents,
                     attachments=ID+".Rmd",
                     test_dir = component_dir+"/yagmail_test")
    else:
        # for sending
        yag=yagmail.SMTP('olsondatascience@gmail.com')
        yag.send(to=email,
                     subject="Homework 2 marks",
                     contents=contents,
                     attachments=ID+".Rmd")