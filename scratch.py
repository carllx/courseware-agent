import urllib.request
import re

url = "https://lite.duckduckgo.com/lite/"
data = urllib.parse.urlencode({'q': 'site:bilibili.com/video 湖人 凯尔特人 俯视'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    bvs = re.findall(r'BV[1-9A-HJ-NP-Za-km-z]{10}', html)
    print("Found:", list(set(bvs)))
except Exception as e:
    print(e)
