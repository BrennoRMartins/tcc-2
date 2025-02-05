from asyncio import sleep
import traceback
import pandas as pd
from googleapiclient.discovery import build
import os 

def get_video_title(api_key, video_id):
    """Fetch the video title for a given video ID."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    title = response['items'][0]['snippet']['title'] if response['items'] else "Unknown Title"
    return title

def get_comments(api_key, video_id, count):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText", maxResults=100)
    df = pd.DataFrame()
    folder_name = 'top_trending'

    # Fetch the title of the video
    video_title = get_video_title(api_key, video_id)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    while request:
        comments = []
        try:
            response = request.execute()
            for item in response['items']:
                # Extract the comment
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Create a new DataFrame and add the video title and comments
            df2 = pd.DataFrame({"video id": video_id, "title": video_title, "comment": comments})
            df = pd.concat([df, df2], ignore_index=True)
            df.to_csv(f"{folder_name}/top_{count}.csv", index=False, encoding='utf-8')

            # Sleep and request the next page of comments
            sleep(2)
            request = youtube.commentThreads().list_next(request, response)
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            print("erro: esperando 10 segundos para continuar")
            sleep(10)
            df.to_csv(f"{folder_name}/top_{count}.csv", index=False, encoding='utf-8')
            break




