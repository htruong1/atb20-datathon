import os
import requests

class atbRequests():
    def __init__(self):
        #self.leapos_username = os.getenv('LEOPOS_USERNAME')
        #self.leapos_password = os.getenv('LEOPOS_PASSWORD')
        self.leapos_username = 'dc6c74fe14787f411e8c7a6'
        self.leapos_password = '27c96d4043fe50M+'
        self.dl_token = self.generate_login_token()

    def generate_login_token(self):
        print("{} {}".format(self.leapos_username, self.leapos_password))
        atb_headers = {
            'Authorization': 'DirectLogin username={},password={},consumer_key={}'.format(self.leapos_username, self.leapos_password, '3c530b772c154927bd3adbe6b058ff75')
        }
        response = requests.post('https://api.leapos.ca/my/logins/direct', headers=atb_headers)
        return response.json().get('token')


    def atbGet(self, url):
        atb_headers = {
            'Authorization' :  'DirectLogin token={}'.format(self.dl_token)
        }
        response = requests.get(url, headers=atb_headers)
        return response.json()
