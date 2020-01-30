#Using API's to extract sample datasets and store them in a DB

#First step in extracting the data is to source it using a web API

#Importing the key libraries to process unstructured data and store them in a pandas dataframe
import pandas as pd
import numpy as np
import requests
import json

#the url variable stores the api link from twitch
url = "https://wind-bow.glitch.me/twitch-api/channels/freecodecamp"

#now let's extract the content in form of a jsn file using the requests lib and take the "dump" a.k.a readeable format
JSONContent = requests.get(url).json()
JSONDump = json.dumps(JSONContent, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=4, separators=None, default=None, sort_keys=False)

#Let's see the formatted json extract
#print(JSONDump)

#Second step is to extract the data from the web API and store it in a pandas dataframe to get a tabular form

#Let's create a list of channels we want to access
channels = ["ESL_SC2", "OgamingSC2", "cretetion", "freecodecamp", "storbeck", "habathcx", "RobotCaleb", "noobs2ninjas",
            "ninja", "shroud", "Dakotaz", "esltv_cs", "pokimane", "tsm_bjergsen", "boxbox", "wtcn", "a_seagull",
           "kinggothalion", "amazhs", "jahrein", "thenadeshot", "sivhd", "kingrichard"]

#Now create an empty list that will be populated with the distinct datasets via a loop
channels_list = []

# For each channel, we access its information through its API
for channel in channels:
    JSONContent = requests.get("https://wind-bow.glitch.me/twitch-api/channels/" + channel).json()
    if 'error' not in JSONContent:
        channels_list.append([JSONContent['_id'], JSONContent['display_name'], JSONContent['status'],
                             JSONContent['followers'], JSONContent['views']])

#Now let's format the array into a panda data frame, assign column names, re-define the index column                         
dataset = pd.DataFrame(channels_list)
dataset.columns = ['Id', 'Name', 'Status', 'Followers', 'Views']
dataset.dropna(axis = 0, how = 'any', inplace = True)
dataset.index = pd.RangeIndex(len(dataset.index))
dataset_5 = dataset.sample(5)
#print(dataset_5)
export_csv = dataset.to_csv(path_or_buf='/home/salexommer/Documents/yellow-submarine/extracts/twitch_sample.csv',index=True)
print("Export completed")