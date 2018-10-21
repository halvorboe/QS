import os
import json

import requests

BASE_URL = 'https://qs.stud.iie.ntnu.no/'

LOGIN_URL = 'loginForm'

email = os.getenv('QS_EMAIL')
password = os.getenv('QS_PASSWORD')

print('--------------------')
print('QS CLI - No cheats')
print('--------------------')

print('logging in...')

r = requests.post(BASE_URL + LOGIN_URL, {'email': email, 'password': password})

if r.status_code != 200:
    raise Exception('Wrong password and username in environ...')

token = r.headers['Set-Cookie'].split(';')[0]

headers = {
    'Host': 'qs.stud.iie.ntnu.no',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': token,
}

print('--------------------')


