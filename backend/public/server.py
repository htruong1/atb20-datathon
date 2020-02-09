from flask import Flask, request
from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from backend.utils.requestutil import atbRequests
from backend.utils.firebaseutil import FirebaseClient
from flask_restplus import reqparse
from backend.public.mock_user_data import mock_src
from backend.utils.transactionutil import TransactionRequest
parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app, title='ATB Hackathon API', description='Web interface version of API')
fb_client = FirebaseClient()
atb_requests = atbRequests()

def queryForAccounts(account_ids):
    account_ids.sort()

    app_user_key = ""

    for account_id in account_ids:
        app_user_key += account_id

    app_user_accounts = {}
    app_user_accounts['appUserId'] = app_user_key
    app_user_accounts['accounts'] = {}
    atb_requests = atbRequests()

    for account_id in account_ids:
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/my/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts/{}/account".format(account_id))
        app_user_accounts['accounts'][account_id] = response

    app_user_accounts['creditScore'] = 'obg'
    return app_user_accounts

@api.route('/api/app/user/info')
class AppAccounts(Resource):
    def put(self):
        account_info = api.payload['accounts']
        app_user_info = queryForAccounts(account_info)
        app_user_info['creditScore'] = account_info['creditScore']
        user_ids = api.payload
        print('Retrieving data for user: {}'.format(user_ids))
        return mock_src
        # account_ids =


@api.route('/api/bank/public/accounts')
class GetPublicAccounts(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts/public")
        return response

@api.route('/api/bank/public/accounts/someid')
class GetPublicAccountById(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/public/accounts/ACCOUNT_ID/owner/account")
        return response

@api.route('/api/bank/accounts')
class GetAccountsAtBanks(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts" )
        return response

@api.route('/api/bank/accounts/someid')
class GetAccountById(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/my/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts/942525966868-10b8be5e-c3e/account")
        return response

@api.route('/api/bank/customers')
class GetCustomers(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/customers")
        return response

@api.route('/api/bank/customers/someid')
class GetCustomerById(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/customers/OBC5252536580-71333")
        return response

@api.route('/api/transaction')
@api.doc("Retrieves all transactions from a given user", params={'acc_id': 'The account ID','bank_id':'The Bank ID'})
class GetAllTransactions(Resource):
    def get(self):
        acc_id = request.args.get("acc_id")
        bank_id = request.args.get("bank_id")
        trans_req = TransactionRequest(bank_id, acc_id)
        trans_req.transaction_request()
        formatted_data = trans_req.format_data()
        return formatted_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
