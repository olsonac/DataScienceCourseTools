import codecs
import json
import re
import pandas as pd
import os

current_directory="/Users/Olsonac-admin/Documents/current/teach/IntroToDataScience/Homework/Homework2c/components/race_policing/marking"
os.chdir(current_directory)

f = codecs.open("plot_nb.ipynb", 'r')
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
        barh_ethnicity_search = re.search("barh_ethnicity\ +:\ +[0-9]+",x2)
        if(barh_ethnicity_search != None):
            barh_ethnicity_score = int(re.sub("barh_ethnicity : ","",barh_ethnicity_search.group()))
            print("barh_ethnicity mark: ",barh_ethnicity_score)
        barh_recoded_eth_search = re.search("barh_recoded_eth\ +:\ +[0-9]+",x2)
        if(barh_recoded_eth_search != None):
            barh_recoded_eth_score = int(re.sub("barh_recoded_eth :","",barh_recoded_eth_search.group()))
            print("barh_recoded_eth mark: ",barh_recoded_eth_score)
        hist_search = re.search("hist_sim_wb_proportions\ +:\ +[0-9]+",x2)
        if(hist_search != None):
            hist_score = int(re.sub("hist_sim_wb_proportions :","",hist_search.group()))
            print("hist_sim_wb_proportions score: ",hist_score)
            result_df.loc[len(result_df)]=[IDstring,barh_ethnicity_score,barh_recoded_eth_score,\
                                      hist_score]
result_df.to_csv("plot_marks.csv",index=False)