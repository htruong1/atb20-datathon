import requests

from backend.utils.requestutil import atbRequests

class TransactionRequest():

    def __init__(self, bank_id, acc_id):
        self.bank_id = bank_id
        self.acc_id = acc_id
        self.request_url = ''
        self.data = None
        self.request_token = atbRequests().generate_login_token()

    def transaction_request(self):
        atb_headers = {
            'Authorization': 'DirectLogin token={}'.format(self.request_token)
        }
        self.request_url = 'https://api.leapos.ca/obp/v4.0.0/my/banks/{}/accounts/{}/transactions'.format(self.bank_id, self.acc_id)
        response = requests.get(self.request_url, headers=atb_headers)
        data = response.json()
        self.data = data
        return self.data

