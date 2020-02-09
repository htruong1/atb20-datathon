import requests

from backend.utils.requestutil import atbRequests

class TransactionRequest():

    def __init__(self, bank_id, acc_id):
        self.bank_id = bank_id
        self.acc_id = acc_id
        self.request_url = ''
        self.data = None
        atbR = atbRequests()
        self.request_token = atbR.generate_login_token()

    def transaction_request(self):
        atb_headers = {
            'Authorization': 'DirectLogin token={}'.format(self.request_token)
        }
        self.request_url = 'https://api.leapos.ca/obp/v4.0.0/my/banks/{}/accounts/{}/transactions'.format(self.bank_id, self.acc_id)
        response = requests.get(self.request_url, headers=atb_headers)
        data = response.json()
        self.data = data
        return self.data

    def format_data(self):
        out_data = []
        for row in self.data.get('transactions'):
            f_data = {
                'type': row.get('details').get('type'),
                'timestamp': row.get('details').get('completed'),
                'description': row.get('details').get('description'),
                'balance': row.get('details').get('new_balance').get('amount'),
                'change': row.get('details').get('value').get('amount')
            }
            out_data.append(f_data)
        return out_data