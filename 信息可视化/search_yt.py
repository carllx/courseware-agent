import urllib.request
import re
from urllib.request import Request, urlopen

url = "https://www.youtube.com/watch?v=1afrzErFy_k"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urlopen(req)
    html = response.read().decode('utf-8')
    title = re.search(r'<title>(.*?)</title>', html).group(1)
    print("1afrzErFy_k:", title)
except: pass

url = "https://www.youtube.com/watch?v=b6VdGHSV6qg"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urlopen(req)
    html = response.read().decode('utf-8')
    title = re.search(r'<title>(.*?)</title>', html).group(1)
    print("b6VdGHSV6qg:", title)
except: pass
