#Now let's replicate the twitch python script to generate a NYT

#Define the key libraries
import pandas as pd
import numpy as np
import requests
import json
import pyjq
from pandas.io.json import json_normalize

#Store the twitch api url and retrieve the raw data
api_key = 'gcpa6XL4z1zLwQXSxW1Y4HniG3zWCWNM'
url = 'https://api.nytimes.com/svc/archive/v1/2020/1.json?&api-key='+api_key
JSONdata = requests.get(url).json()

#Check the total number of articles in the data extract
JSONdataheader = pyjq.all('.copyright',JSONdata) 
JSONdoccount = pyjq.all('.response .docs | length',JSONdata)[0]

#now let's extract the relevant fields only
JSONdataextract = f'.response .docs [] | {{the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date, the_news_desk: .news_desk}}'
JSONdataextractoutput = pyjq.all(JSONdataextract, JSONdata)
JSONdataextractoutput_dump = json.dumps(JSONdataextractoutput,indent=4)
#print(JSONdataextractoutput_dump)
#print("The total number of documents is " + str(JSONdoccount))

#creating a json extract and keeping it locally
jsonurl = '/home/salexommer/Documents/yellow-submarine/extracts/nyt_month_data.json'
df = pd.read_json(jsonurl, orient='columns')

#re-transforming the json into a csv table
export_csv = df.to_csv(path_or_buf='/home/salexommer/Documents/yellow-submarine/extracts/nyt_snippet_sample.csv',index=True)
print("The total number of extracted NYT snippets stored in a csv is " + str(JSONdoccount))