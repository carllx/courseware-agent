import requests
url = 'https://jwxt.nfu.edu.cn/jwglxt/kbcx/jskbcxMobile_cxJsKb1.html?gnmkdm=N2152'
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'JSESSIONID=CDFB60DC5CF345E25162CC69FB0A3281; route=384b36dd9add5fa6af1020180dd3e5a2',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
}
try:
    r = requests.post(url, headers=headers, data='xnm=2025&doType=app&xqm=12&kblx=2&jgh=', timeout=5, verify=False)
    print(r.status_code)
    print(r.text[:200])
except Exception as e:
    print(e)
