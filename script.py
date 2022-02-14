
"""Input --The script uses recursion to parse FB's JSON dump.
Output --The script spits out single csv per JSON.
root --The directory's path containing all the folders coming from FB; dtype=string. 
output_loc --The path of desired location to store csvs; dtype=string.
"""

import os
import pandas as pd
import json
   
#Input dir path containing all folders coming from FB
root = "/home/nouman/Desktop/fb_parse/facebook-100007711683137/"
folders = os.listdir(root)

# Output dir that will contain csvs
os.makedirs("/home/nouman/Desktop/fb_parse/"+"parsed_csvs",exist_ok=True)

# Let's recursively parse each JSON present in each folder 
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
            csv_file_name= file_name.split(".")[0] # to remove .json from the parsed dir names
            
            with open(root+directory+'/'+file_name, "r") as read_file:

                developer = json.load(read_file)

            dic={}  
            def parse_json_recursively(json_object):

                if type(json_object) is dict:

                    for index,key in enumerate(json_object):
                        parse_json_recursively(json_object[key])

                        if (type(json_object[key]) is not dict) and (type(json_object[key]) is not list):
                            #if key=='timestamp':
                                #continue
                            if key not in dic:
                                dic[key]=[]

                            if index==0:
                                dic[key].append(json_object[key])
                            elif key in dic:
                                dic[key].append(json_object[key])



                elif type(json_object) is list:
                    for item in json_object:
                        parse_json_recursively(item)
                #p. loc. exception list not having dic but a list
            
            parse_json_recursively(developer)

            df=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dic.items() ]))
            
            #df=df[~(df.duplicated('timestamp'))].reset_index(drop=True)
            #df.dropna(axis=1,thresh=20)
            
            output_loc= "/home/nouman/Desktop/fb_parse/parsed_csvs/"+file_name+'.csv'  
            df.to_csv(output_loc)   
            #print(df)


print(__doc__)        