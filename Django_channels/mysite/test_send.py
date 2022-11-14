import json
import urllib.request

url = "http://127.0.0.1:8000/home/change_stat"  # URL

d = {'cam_id': 1, 'trash': False, 'intrusion': False, 'fallen': False, 'fence':False}
params = json.dumps(d).encode("utf-8")  
req = urllib.request.Request(url, data=params,
                             headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))  
