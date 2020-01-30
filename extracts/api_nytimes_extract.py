#Now let's replicate the twitch python script to generate a NYT

#Define the key libraries
import pandas as pd
import numpy as np
import requests
import json

#Store the twitch api url
api_key = 'gcpa6XL4z1zLwQXSxW1Y4HniG3zWCWNM'
url = 'https://api.nytimes.com/svc/archive/v1/2020/1.json?&api-key='+api_key
JSONdata = requests.get(url).json()
JSONdatadump = json.dumps(JSONdata,indent=4)
print(JSONdatadump)