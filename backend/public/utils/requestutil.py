import os
import requests

class atbRequests():
    def __init__(self):
        self.dl_token = os.getenv('ATB_TOKEN')

    def atbGet(self, url):
        atb_headers = {
            'Authorization' :  'DirectLogin token={}'.format(self.dl_token)
        }

        response = requests.get(url, headers=atb_headers)
        return response.json()
