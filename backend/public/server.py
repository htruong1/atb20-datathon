from flask import Flask, request, abort
import random
from flask_restplus import Resource, Api, fields
from backend.utils.requestutil import atbRequests
from backend.utils.firebaseutil import FirebaseClient
from flask_restplus import reqparse
from backend.utils.transactionutil import TransactionRequest
parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app, title='ATB Hackathon API', description='Web interface version of API')
fb_client = FirebaseClient()
atb_requests = atbRequests()

def get_donation_estimate(acc_id, bank_id):
    try:
        trans_req = TransactionRequest(bank_id, acc_id)
        trans_req.transaction_request()
        formatted_data = trans_req.format_data()
    except TypeError as e:
        return {"Error": "Invalid acc or bank id"}
    sum_transactions = 0
    balance_info = []
    curr_balance = float(formatted_data[0].get('balance'))
    for transaction in formatted_data:
        next_transaction = float(transaction.get('balance'))
        balance_info.append({
            'balance': transaction.get('balance'),
            'timestamp': transaction.get('timestamp')
        })
        if next_transaction < 0:
            # 336 = 324 - (7 - -19)
            sum_transactions = sum_transactions - (curr_balance - next_transaction)
            curr_balance = next_transaction
        elif curr_balance - next_transaction < 0:
            sum_transactions -= (curr_balance - next_transaction)
            curr_balance = next_transaction
        elif curr_balance - next_transaction > 0:
            sum_transactions += (curr_balance - next_transaction)
            curr_balance = next_transaction
        else:
            continue

    donation_data = {
        "net_change": sum_transactions,
        "ending_balance": curr_balance
    }

    return donation_data, balance_info


def queryForAccounts(account_ids):
    account_ids.sort()
    app_user_key = ""
    for account_id in account_ids:
        app_user_key += account_id
    app_user_accounts = {}
    app_user_accounts['appUserId'] = app_user_key
    app_user_accounts['accounts'] = {}
    bank_ids = {}
    for account_id in account_ids:
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/my/banks/dc6c74fe14787f411e8c7a6c3991fe8/accounts/{}/account".format(account_id))
        if response.get('code') != 400:
            app_user_accounts['accounts'][account_id] = response
            bank_ids[response['bank_id']] = account_id
    for bank_id in bank_ids.keys():
        don_est, trans_history = get_donation_estimate(bank_ids[bank_id],bank_id)
        app_user_accounts['accounts']['donation_est'] = don_est
        app_user_accounts['accounts']['transaction_history'] = trans_history
    app_user_accounts['creditScore'] = random.randint(0,900)
    return app_user_accounts



@api.route('/api/app/user/info')
class AppAccounts(Resource):
    resource_fields = api.model('acc_id', {
        'accounts': fields.String
    })
    @api.expect(resource_fields)
    def put(self):
        try:
            account_info = api.payload['accounts']
            if account_info == "kryalls":
                account_info = ["4493339090308-5ce80523-4d4", "9043171164440-086540fa-449", "5090619851098-e186c945-3d4", "4052095672593-266926ce-c71", "479519821612-dac5b8c8-10c"]
            elif account_info == 'ewinson':
                account_info = ["5090690952535-c1b5ed8a-998","942597818971-ceb100da-d60","5090620572706-5ed9eea5-485","4052029034692-bf1422ca-4e0","3962389777643-f90bdaf5-6e1"]
            elif account_info == 'htruong':
                account_info = ["3962379603916-4a5659cb-e48", "4493313863214-69a410cd-e80", "479509075209-9354a225-fd0", "4252851126039-214b0466-00f", "5532144418747-dd3de0e1-432"]

        except TypeError:
            abort(400, 'Invalid account json array')
        app_user_info = queryForAccounts(account_info)
        print('Retrieving data for users: {}'.format(account_info))
        return app_user_info


@api.route('/api/bank/public/accounts',doc=False)
class GetPublicAccounts(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts/public")
        return response

@api.route('/api/bank/public/accounts/someid',doc=False)
class GetPublicAccountById(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/public/accounts/ACCOUNT_ID/owner/account")
        return response

@api.route('/api/bank/accounts',doc=False)
class GetAccountsAtBanks(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts" )
        return response

@api.route('/api/bank/accounts/someid',doc=False)
class GetAccountById(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/my/banks/3621ab3c23c3b1425fb18ee80a6a7ed/accounts/942525966868-10b8be5e-c3e/account")
        return response

@api.route('/api/bank/customers',doc=False)
class GetCustomers(Resource):
    def get(self):
        atb_requests = atbRequests()
        response = atb_requests.atbGet("https://api.leapos.ca/obp/v4.0.0/banks/3621ab3c23c3b1425fb18ee80a6a7ed/customers")
        return response

@api.route('/api/bank/customers/someid',doc=False)
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
        try:
            trans_req = TransactionRequest(bank_id, acc_id)
            trans_req.transaction_request()
            formatted_data = trans_req.format_data()
        except TypeError as e:
            return {"Error": "Invalid acc or bank id"}
        return formatted_data

@api.route('/api/donation',doc=False)
@api.doc("Calculates donation amount for a given user", params={'acc_id': 'The account ID','bank_id':'The Bank ID'})
class GetDonationAmount(Resource):
    def get(self):
        acc_id = request.args.get("acc_id")
        bank_id = request.args.get("bank_id")
        try:
            trans_req = TransactionRequest(bank_id, acc_id)
            trans_req.transaction_request()
            formatted_data = trans_req.format_data()
        except TypeError as e:
            return {"Error": "Invalid acc or bank id"}
        sum_transactions = 0
        curr_balance = float(formatted_data[0].get('balance'))
        for transaction in formatted_data:
            next_transaction = float(transaction.get('balance'))
            if next_transaction < 0:
                # 336 = 324 - (7 - -19)
                sum_transactions = sum_transactions - (curr_balance - next_transaction)
                curr_balance = next_transaction
            elif curr_balance - next_transaction < 0:
                sum_transactions -= (curr_balance - next_transaction)
                curr_balance = next_transaction
            elif curr_balance - next_transaction > 0:
                sum_transactions += (curr_balance - next_transaction)
                curr_balance = next_transaction
            else:
                continue
        return {
            "net_change": sum_transactions,
            "ending_balance": curr_balance
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
