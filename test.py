import requests
import time


def keepconnect():
    while True:
        time.sleep(60)
        request = requests.post(
            'https://fxcm-webhook-av6kzliihq-uc.a.run.app/fxcmcheck', data='check')
        print(request.json())
        return request.json()
