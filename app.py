import requests
BASE = "http://13.201.75.30"

response6 = requests.get(BASE + '/api/login', json = {'id' : 'mehul12', 'pwd' : 'xx'}, timeout=100)

print(response6.json())