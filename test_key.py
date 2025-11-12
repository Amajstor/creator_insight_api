import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('YOUTUBE_API_KEY')
TEST_CHANNEL = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel

print(f"Testing API Key: {API_KEY[:10]}...")

url = "https://www.googleapis.com/youtube/v3/channels"
params = {
    'part': 'snippet,statistics',
    'id': TEST_CHANNEL,
    'key': API_KEY
}

try:
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")