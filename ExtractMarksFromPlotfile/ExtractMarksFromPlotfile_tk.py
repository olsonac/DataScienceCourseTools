import codecs
import json
import re
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog,Label,Button


class ExtractMarksFromPlotfile:
    def __init__(self, master):
        self.master = master
        self.MyInputFilename = ""

        self.label = Label(master, text="Pick input file with plot information)")
        self.label.pack()

        self.InputFile_button = Button(master, text="Pick input file with plot information (usually plot_nb.ipynb)", command=self.GetInputFilenames)
        self.InputFile_button.pack()

        self.Concat_button = Button(master, text="Extract plot information", command=self.ExtractMarks)
        self.Concat_button.pack()

    def ExtractMarks(self):
        InputFilename = ExtractMarksFromPlotfile.MyInputFilename
        InputFolder = os.path.dirname(InputFilename)
        os.chdir(InputFolder)

        f = codecs.open(InputFilename, 'r')
        source = f.read()

        y = json.loads(source)
        pySource = ''
        result_df=pd.DataFrame(columns = ["ID","barh_eth","barh_recoded","hist"])
        for x in y['cells']:
             for x2 in x['source']:
                ID_search = re.search("##\ +[a-z]+[0-9]+",x2)
                if(ID_search != None):
                    IDstring = re.sub("## ","",ID_search.group())
                    print("ID: -",IDstring,"-")
                barh_ethnicity_search = re.search("barh_ethnicity\ +:\ +[0-9]+\.*[0-9]*",x2)
                if(barh_ethnicity_search != None):
                    barh_ethnicity_score = float(re.sub("barh_ethnicity : ","",barh_ethnicity_search.group()))
                    print("barh_ethnicity mark: ",barh_ethnicity_score)
                barh_recoded_eth_search = re.search("barh_recoded_eth\ +:\ +[0-9]+\.*[0-9]*",x2)
                if(barh_recoded_eth_search != None):
                    barh_recoded_eth_score = float(re.sub("barh_recoded_eth :","",barh_recoded_eth_search.group()))
                    print("barh_recoded_eth mark: ",barh_recoded_eth_score)
                hist_search = re.search("hist_sim_wb_proportions\ +:\ +[0-9]+\.*[0-9]*",x2)
                if(hist_search != None):
                    hist_score = float(re.sub("hist_sim_wb_proportions :","",hist_search.group()))
                    print("hist_sim_wb_proportions score: ",hist_score)
                    result_df.loc[len(result_df)]=[IDstring,barh_ethnicity_score,barh_recoded_eth_score,\
                                              hist_score]
        result_df.to_csv("plot_marks.csv",index=False)
        self.master.quit()
        self.master.destroy()

    def GetInputFilenames(self):
        ExtractMarksFromPlotfile.MyInputFilename=\
            filedialog.askopenfilename(initialdir = ".", \
                                        title = "Select file", \
                                        filetypes = ((".ipynb files","*.ipynb"),("all files","*.*")))
root = tk.Tk()
my_concat_wav = ExtractMarksFromPlotfile(root)
root.title("Extract plot information from plot_nd_ipynb")
root.mainloop()