#Using API's to extract sample datasets and store them in a DB

#Importing the key libraries to process unstructured data and store them in a dataframe
import pandas as pd
import numpy as np
import requests
import json

url = "https://wind-bow.glitch.me/twitch-api/channels/freecodecamp"
JSONContent = requests.get(url).json()
JSONDump = json.dumps(JSONContent, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=4, separators=None, default=None, sort_keys=False)
print(JSONDump)