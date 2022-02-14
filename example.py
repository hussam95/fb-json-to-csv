
"""Input -- JSON file
Intermediate output -- 1 or mroe csvs per JSON depending on level of nesting
Final output -- 1 concatenated csv per JSON
root -- Path of directory containing FB's JSON dump files
"""

import fbjson2table
from tabulate import tabulate
from fbjson2table.table_class import TempDFs
from fbjson2table.func_lib import parse_fb_json
import os
import glob
import pandas as pd


root = "/home/nouman/fb-json2table/Data/facebook-100007711683137/"
folders = os.listdir(root)

# Let's create a csv at each level of nesting for every JSON
# Let's save all the csvs per JSON into a separate directory named after JSON
for folder in folders:
    directory = folder
    path= os.path.join(root,directory)
    file= os.listdir(path)
    if (len(file)==1) and (file[0]=="no-data.txt"):
        continue
    elif (len(file)==1) and (file[0]=="media"):
        continue
    else:
        counter = len(file)
        for i in range(counter):
            file_name= file[i]
            file_name= file_name.split(".")[0] # to remove .json from the parsed dir names
            os.makedirs('/home/nouman/fb-json2table/Data/parsed_'+file_name, exist_ok=True)
        
            json_content = parse_fb_json(root+directory+'/'+file[i])
            temp_dfs = TempDFs(json_content)

            for df, table_name in zip(temp_dfs.df_list, temp_dfs.table_name_list):
                #print(table_name,':')
                #print(tabulate(df, headers='keys', tablefmt='psql'), '\n')  
                df.to_csv('/home/nouman/fb-json2table/Data/parsed_'+file_name+'/'+table_name+'.csv')   
                
                
# Let's concatenate all csvs per JSON to a single csv

root = "/home/nouman/fb-json2table/Data/"
folders = os.listdir(root)
folders
all_data={}

for folder in folders:
    if folder == "facebook-100007711683137":
        continue
    else:
        path=r"/home/nouman/fb-json2table/Data/"+folder
        all_files= glob.glob(path+"/*.csv")
        
        li = []
        
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)

        frame = pd.concat(li, axis=1, ignore_index=False)
        all_data[folder]=frame

# Let's save single csv per JSON (with concatenated pre-script) in a directory called concatenated_csvs         
os.makedirs("/home/nouman/fb-json2table/concatenated_csvs", exist_ok=True)
new_key=""

for key in all_data:
    splitted=key.split("_")
    for index, word in enumerate(splitted):
        if index==0:
            new_key="concatenated_"
        else:
            new_key+=word+'_'
            
    dic= all_data[key]
    df= pd.DataFrame(dic)
    df.to_csv("/home/nouman/fb-json2table/concatenated_csvs/"+new_key+'csv')
    
print(__doc__)