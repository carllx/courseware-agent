import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://html.duckduckgo.com/html/?q=Reuters+Florida+gun+deaths+chart+inverted'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

img_url = None
for a in soup.find_all('a', class_='imageResult'):
    img_url = a.get('href')
    if img_url:
        break

if not img_url:
    print("Could not find image via DuckDuckGo")
    # Fallback to a known URL that usually works
    img_url = "https://i.insider.com/534ebca4ecad04871e626887"

print(f"Downloading from: {img_url}")

try:
    img_data = requests.get(img_url, headers=headers).content
    os.makedirs('信息可视化/weeks/W07_Project_Design/public/slides', exist_ok=True)
    with open('信息可视化/weeks/W07_Project_Design/public/slides/m00_reuters_gun_deaths.png', 'wb') as handler:
        handler.write(img_data)
    print("Downloaded successfully.")
except Exception as e:
    print(f"Error downloading: {e}")
