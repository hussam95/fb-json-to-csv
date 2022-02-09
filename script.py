import os
import pandas as pd
import json

            
root = "/home/nouman/Desktop/fb_parse/facebook-100007711683137/"
folders = os.listdir(root)

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

                    for key in json_object:
                        parse_json_recursively(json_object[key])

                        if (type(json_object[key]) is not dict) and (type(json_object[key]) is not list):
                            #if key=='timestamp':
                                #continue
                            if key in dic:
                                dic[key].append(json_object[key])

                            else:
                                dic[key]=[]


                elif type(json_object) is list:
                    for item in json_object:
                        parse_json_recursively(item)

            parse_json_recursively(developer)

            pd.set_option('display.max_rows',None)
            df=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dic.items() ]))
            #df=df[~(df.duplicated('timestamp'))].reset_index(drop=True)
            #df.dropna(axis=1,thresh=20)
            df.to_csv(root+csv_file_name+'.csv')   
            #print(df)

        
            

            
            
            
             