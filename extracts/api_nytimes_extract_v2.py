#Define the key libraries
from datetime import date
import pandas as pd
import numpy as np
import requests
import json
import pyjq
import os
#Test comment
#define this month's variable
today = date.today()
m1 = int(today.strftime("%m")) #current month
y1 = int(today.strftime("%Y")) #current year
y2 = y1 - 0 #two years ago from today --temporarily set to 0 if required
y3 = int(today.strftime("%Y")) #current year
y4 = y3 - y2 #number of years

#Store the twitch api url and retrieve the raw data
api_key = 'gcpa6XL4z1zLwQXSxW1Y4HniG3zWCWNM'
csv_path = './yellow-submarine/extracts/'

#A loop to cycle through years & set month
while y1 >= y2:
    if y1 == y3:
        m2 = m1 #variable month for the loop
    else:
        m2 = 12
    print("Extracting two years worth of data from NYT for year "+str(y1))
    
    #A loop to cycle through months & set year
    while m2 >= 1:
        print("...extracting the data for " + str(m2) + "/"+ str(y1))
        url = 'https://api.nytimes.com/svc/archive/v1/'+str(y1)+'/'+str(m2)+'.json?&api-key='+api_key
        JSONdata = requests.get(url).json()
        JSONdoccount = pyjq.all('.response .docs | length',JSONdata)[0]
        JSONdataextract = f'.response .docs [] | {{the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date, the_news_desk: .news_desk}}'
        JSONdataextractoutput = pyjq.all(JSONdataextract, JSONdata)
        JSONdataextractoutput_dump = json.dumps(JSONdataextractoutput,indent=4)

        #creating a json extract and keeping it locally
        with open(csv_path+'nyt_month_data_'+str(m2)+str(y1)+'.json','w') as fi:
            fi.write(JSONdataextractoutput_dump)
        jsonurl =csv_path+'nyt_month_data_'+str(m2)+str(y1)+'.json'
        
        #re-transforming the json into a Pandas DataFrame and exporting it as a csv
        df = pd.read_json(jsonurl, orient='columns')
        #df.columns = ['index', 'snippet', 'the_headline','pub_date','news_desk']
        export_csv = df.to_csv(path_or_buf=csv_path+'nyt_snippet_sample_'+str(m2)+str(y1)+'.csv',index=True, index_label="id")
        print("The total number of extracted NYT snippets stored in this csv for "+ str(m2) + "/"+ str(y1)+ ' is ' + str(JSONdoccount))
        m2 = m2 - 1

        #Remove the temporary JSON files
        if os.path.exists(jsonurl):
            os.remove(jsonurl)
        else:
            print("The file doesn't exist.")
    else:
        y1 = y1 - 1
else:
    if y4 == 0:
        print("Snippets for the current year have been extracted.")    
    else:
        print("Snippets for the past "+ str(y4) +" years have been extracted.")