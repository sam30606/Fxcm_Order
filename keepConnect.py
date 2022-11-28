import requests
import time


while True:
    request = requests.post(
        'https://fxcm-webhook-av6kzliihq-uc.a.run.app/fxcmcheck', data='check')
    if request:
        print(request.json())
    else:
        print("noResponse")
    time.sleep(60)
