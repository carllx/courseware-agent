import urllib.request
import json
import urllib.parse
from urllib.request import Request, urlopen

def search_bili(keyword):
    print(f"--- Search: {keyword} ---")
    url = "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=" + urllib.parse.quote(keyword)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
        data = json.loads(response.read())
        results = data.get('data', {}).get('result', [])
        for module in results:
            if module.get('result_type') == 'video':
                for v in module.get('data', [])[:3]:
                    print(f"Title: {v.get('title').replace('<em class=\"keyword\">', '').replace('</em>', '')}")
                    print(f"URL: https://www.bilibili.com/video/{v.get('bvid')}")
                    print(f"Duration: {v.get('duration')}")
    except Exception as e:
        pass

search_bili("Shannon's Information Entropy")
search_bili("Information Entropy Art of the Problem")
