import os
import requests
import polars as pl
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.googleapis.com/youtube/v3"
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_video_id_data() -> str:
    request_url = f"{BASE_URL}/search"
    
    video_ids = []
    page_token = ''

    while True:    
        request_params = {
            "key" : API_KEY,
            "channelId" : CHANNEL_ID,
            "part" : "snippet",
            "maxResults" : 50,
            "order" : "date",
            "pageToken" : ""
        }   

        if page_token:
            request_params["pageToken"] = page_token

        try:
            response = requests.get(request_url, params=request_params)
            response.raise_for_status()

            response_data = response.json()

            items = response_data.get("items", [])

            video_ids.extend([item.get("id", {}).get("videoId", "") for item in items])

            page_token = response_data.get("nextPageToken", "")

            if not page_token:
                break

        except requests.exceptions.HTTPError as err_h:
            print(f"HTTP error: {err_h}")
        except requests.exceptions.RequestException as err_r:
            print(f"Request error: {err_r}")

    return video_ids

def get_video_data(video_id_list: list) -> list:
    request_url = f"{BASE_URL}/videos"
    
    video_data = []

    for i in range(0, len(video_id_list), 50):
        video_batch = video_id_list[i:i+50]
        id_string = ",".join(video_batch)


        request_params = {
            "key" : API_KEY,
            "id" : id_string,
            "part" : "snippet, contentDetails, statistics, topicDetails"
        }

        try:
            response = requests.get(request_url, params=request_params)
            response.raise_for_status()

            response_data = response.json().get("items", [])

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
        except requests.exceptions.HTTPError as err_h:
            print(f"HTTP Error: {err_h}")

    return video_data

def main() -> None:
    video_id_data = get_video_id_data()
    video_data = get_video_data(video_id_data)
    
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pl.DataFrame(video_data)
    df.write_parquet(f"{run_time}-data.parquet")

if __name__ == "__main__":
    main() 
