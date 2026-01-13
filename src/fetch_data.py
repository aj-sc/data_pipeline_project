import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/youtube/v3"
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_video_ids():
    request_url = f"{BASE_URL}/search"
    
    request_params = {
        "key" : API_KEY,
        'channelId' : CHANNEL_ID,
        'part' : 'snippet',
        'maxResults' : 50,
        'order' : 'date',
    }

    response = requests.get(request_url, params=request_params)

    return response.json()

    

def get_video_data():
    request_url = f"{BASE_URL}/videos"

    request_params = {}

    response = requests.get(request_url, params=request_params)

    pass

data = get_video_ids()

print(data)
