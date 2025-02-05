from importlib.metadata import files
import json
import requests
import comments_trends as ct

url = "https://www.searchapi.io/api/v1/search"
params = {
  "engine": "youtube_trends",
  "gl": "br",
  "bp": "films",
  "api_key": "vjQEPo6yS4T8QeypJVHK9hmc"
}

ids = []

yt_api_key = "AIzaSyBX_81NTz0lNuc5xjPoLZcfm-b-VRbnDc8"

response = requests.get(url, params = params)
data = response.json()

trends = data.get('trending', [])
for item in trends:
    dict = {"Title": item['title'],"Position": item['position'], "Video_id":item['id']}
    ids.append(dict)
print(ids)

with open("trending_videos.json", "w", encoding="utf-8") as final:
	json.dump(ids, final,ensure_ascii=False, indent=4)

with open('trending_videos.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

count = 0
for video in dados:
     count = count + 1
     ct.get_comments(yt_api_key,video['Video_id'], count)