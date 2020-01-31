#Now let's replicate the twitch python script to generate a NYT

#Define the key libraries
import pandas as pd
import numpy as np
import requests
import json
import pyjq

#Store the twitch api url and retrieve the raw data
api_key = 'gcpa6XL4z1zLwQXSxW1Y4HniG3zWCWNM'
url = 'https://api.nytimes.com/svc/archive/v1/2020/1.json?&api-key='+api_key
JSONdata = requests.get(url).json()
#JSONdatadump = json.dumps(JSONdata,indent=4)
#print(JSONdatadump)

#Check the total number of articles in the data extract
JSONdataheader = pyjq.all('.copyright',JSONdata) 
JSONdoccount = pyjq.all('.response .docs | length',JSONdata)[0]
#print("The total number of documents is " + str(JSONdoccount))

#now let's extract the relevant fields only
JSONdataextract = f'.response .docs [] | {{the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date, the_news_desk: .news_desk}}'
JSONdataextractoutput = pyjq.all(JSONdataextract, JSONdata)
JSONdataextractoutput_dump = json.dumps(JSONdataextractoutput,indent=4)
print(JSONdataextractoutput_dump)

#Let's create a different list that contains the values only
documents = ["the_snippet", "the_headline","the_date","the_news_desk"]
document_list = []
for document in documents:
    if 'error' not in JSONdataextractoutput:
        document_list.append([
        JSONdataextractoutput['the_snippet'],
        JSONdataextractoutput['the_headline'],
        JSONdataextractoutput['the_date'],
        JSONdataextractoutput['the_news_desk']])

#Finally structure the dataset in a pandas dataframe
PANDASdataset = pd.DataFrame(document_list)
PANDASdataset.columns = ['ID','Snippet', 'Headline', 'Publication Date', 'News Section']
PANDASdataset.dropna(axis=0, how='any',inplace=True)
#PANDASdataset.index = pd.RangeIndex(len(PANDASdataset.index))
print(PANDASdataset)
#test comment to see how we can push stuff into the repo