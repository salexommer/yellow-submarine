#Define the key libraries
from datetime import date
import pandas as pd
import numpy as np
import requests
import json
import pyjq

#define this month's variable
today = date.today()
m1 = int(today.strftime("%m")) #current month
y1 = int(today.strftime("%Y")) #current year
y2 = y1 - 2 #two years ago from today

#Store the twitch api url and retrieve the raw data
api_key = 'gcpa6XL4z1zLwQXSxW1Y4HniG3zWCWNM'

#create a loop to cycle through years
while y1 >= y2:
    m2 = m1 #variable month for the loop
    print("Extracting two years worth of data from NYT")

    #create a loop to cycle through months
    while m2 >= 1:
        print("...extracting the data for " + str(m2) + "/"+ str(y1))
        url = 'https://api.nytimes.com/svc/archive/v1/'+str(y1)+'/'+str(m2)+'.json?&api-key='+api_key
        JSONdata = requests.get(url).json()
        JSONdataheader = pyjq.all('.copyright',JSONdata) 
        JSONdoccount = pyjq.all('.response .docs | length',JSONdata)[0] #split the JSON by batches
        JSONdataextract = f'.response .docs [] | {{the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date, the_news_desk: .news_desk}}'
        JSONdataextractoutput = pyjq.all(JSONdataextract, JSONdata)
        JSONdataextractoutput_dump = json.dumps(JSONdataextractoutput,indent=4)
        #creating a json extract and keeping it locally
        with open('/home/salexommer/Documents/yellow-submarine/extracts/nyt_month_data_'+str(m2)+str(y1)+'.json','w') as fi:
            fi.write(JSONdataextractoutput_dump)
        jsonurl = '/home/salexommer/Documents/yellow-submarine/extracts/nyt_month_data_'+str(m2)+str(y1)+'.json'
        df = pd.read_json(jsonurl, orient='columns')
        #re-transforming the json into a csv table
        export_csv = df.to_csv(path_or_buf='/home/salexommer/Documents/yellow-submarine/extracts/nyt_snippet_sample_'+str(m2)+str(y1)+'.csv',index=True)
        print("The total number of extracted NYT snippets stored in this csv for "+ str(m2) + "/"+ str(y1)+ ' is ' + str(JSONdoccount))
        m2 = m2 - 1
    y1 = y1 - 1
    m1 = 12
print("Snippets for the past 2 years have been extracted.")