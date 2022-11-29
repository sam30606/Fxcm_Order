import requests
import time


while True:
    request = requests.post(
        'https://fxcm-webhook-av6kzliihq-uc.a.run.app/fxcmcheck', data='check')
    if request:
        print(request.json(), time.ctime())
    else:
        print("noResponse", time.ctime())
    time.sleep(30)
