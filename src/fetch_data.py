import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/youtube/v3"
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_video_id_string() -> str:
    request_url = f"{BASE_URL}/search"
    
    request_params = {
        "key" : API_KEY,
        'channelId' : CHANNEL_ID,
        'part' : 'snippet',
        'maxResults' : 50,
        'order' : 'date',
    }

    response = requests.get(request_url, params=request_params)
    
    response_data = response.json().get("items", {})

    video_ids = [item.get("id", {}).get("videoId", "") for item in response_data]
    
    id_string = ",".join(video_ids)

    return id_string

def get_video_data(id_string: str):
    request_url = f"{BASE_URL}/videos"

    request_params = {
        "key" : API_KEY,
        "id" : id_string,
        "part" : "snippet, contentDetails, statistics, topicDetails"
    }

    response = requests.get(request_url, params=request_params)
    
    response_data = response.json().get("items", [])

    video_data = []

    for video in response_data:
        video_data.append(
            {
                "video_id" : video.get("id", ""),
                "video_title" : video.get("snippet", {}).get("title", ""),
                "published_at" : video.get("snippet", {}).get("publishedAt", ""),
                "views" : video.get("statistics", {}).get("viewCount", ""),
                "likes" : video.get("statistics", {}).get("likeCount", ""),
                "comments" : video.get("statistics", {}).get("commentCount", ""),
                "favorites" : video.get("statistics", {}).get("favoriteCount", ""),
                "topics" : video.get("topicDetails", {}).get("topicCategories", [])
            }
        )

    return video_data
    

id_string = get_video_id_string()
video_data = get_video_data(id_string)

print(video_data)
