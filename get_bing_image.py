import urllib.request
import urllib.parse
import re
import json

def search_image(query):
    # Use duckduckgo html
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # We need an image, DDG html doesn't show large images easily. 
    except Exception as e:
        print(e)

# Let's search wikipedia or just flickr
def get_wiki_image():
    # search wikipedia API for tesla model 3 interior
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=images&titles=Tesla_Model_3&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read()
    data = json.loads(res)
    pages = data['query']['pages']
    for page_id in pages:
        for img in pages[page_id].get('images', []):
            if 'interior' in img['title'].lower() or 'screen' in img['title'].lower() or 'dashboard' in img['title'].lower():
                print("Found WP img:", img['title'])
    
get_wiki_image()
