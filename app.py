import requests
# import webbrowser
BASE = "http://127.0.0.1:5000/"

response6 = requests.get(BASE + '/api/get_data', json = {'id' : 'mehul12', 'pwd' : 'xx'})

print(response6.json())