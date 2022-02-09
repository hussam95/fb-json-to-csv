# Facebook JSON TO CSV Using Recursive Function

## Background
Facebook allows users to [downlaod](https://www.facebook.com/help/1701730696756992) their data either in form of HTML or JSON files. Dealing with data in JSON or HTML format often gets tricky. Moreover, data manipulation for these files is also harder.
In order to make the FB dump more productive from a development point of view, ideally we would want all the JSONs of the dump to be in a format that is more manuverable.

The script.py is specifically written to solve this problem. It will allow you to convert JSON dump coming from FB to ready-to-use csvs (one csv per JSON file). If you are looking to apply some machine learning techniques to your FB data, this script can help you in setting up the ETL pipeline.


## Method

The script uses a recursive function to parse the nested JSON files. The idea behind recursive funciton is fairly simple: continue expanding/flattening the JSON file untill you reach the leaves or keys that have non-list and non-dict values. 
